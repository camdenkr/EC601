# Used to gather social media sentiment analysis for a specific Twitter user
import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from requests.api import head

import os
from google.cloud import language_v1



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"


'''
Returns the twitter unique user id associated with a username.
:username: a Twitter username string
'''
def get_userID(username):
    userID = ""

    url = "https://api.twitter.com/2/users/by/username/" + str(username)

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }

    response = requests.request("GET", url, headers = headers, params = None)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    # raise Exception()
    if('errors' in response.text):
        raise Exception(response.json()["errors"])
    return response.json()["data"]["id"]


'''
Returns a json of a user's Tweets. The user is specified by user_id which can be gathered from a username using
get_userID(). By default retrieves the [max_number] (default of 10) most recent tweets
:param user_id: Unique Twitter User ID
'''
def get_user_tweets(user_id, start_time=None, end_time=None, max_results=10, pagination_token=None):
    assert (max_results<=100)

    url = "https://api.twitter.com/2/users/" + user_id + "/tweets"
    

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }
    
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'pagination_token': pagination_token,
        # 'user.fields': "created_at"
    }
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


"Takes in a tweet ID and identifies when it was created"
def tweet_date_lookup(tweetID):
    
    url = "https://api.twitter.com/2/tweets/" + tweetID
    

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }

    params = {
        "tweet.fields": "created_at"
    }
    
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()["data"]["created_at"]

'''
Retrieves a total number of tweets and their respective dates as specified
:param userID: unique Twitter ID for a user
:param n_retrieval: number of tweets to retrieve
'''
def get_tweets(userID, n_retrieval):
    # We want to retrieve 100 tweets, so keep searching while the number of tweets 
    # gather is less than 100 or we are out of tweets, appending to total tweets
    tweets_text, tweets_date = [], []
    token = None
    while( len(tweets_text)<=n_retrieval or not ("next_token" in tweets["meta"]) ):
        tweets = get_user_tweets(userID, pagination_token=token)
        token = tweets["meta"]["next_token"]
        for tweet in tweets["data"]:
            tweets_text.append(tweet["text"])
            tweets_date.append(tweet_date_lookup(tweet["id"]))
            if(len(tweets_text)>=n_retrieval):
                break
    return tweets_text, tweets_date




def analyze_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    sentiment = response.document_sentiment.score
    magnitude = response.document_sentiment.magnitude


    return sentiment, magnitude

'''
Call function to retrieve sentiment analysis from Google NLP for each tweets in the list
:param tweets: a list of strings
:return sentiments: sentiment score for each string in tweets
:return magnitudes: senttiment magnitude for each sentiment in sentiments
'''
def get_sentiments(tweets):
    sentiments, magnitudes = [], []

    for tweet in tweets:
        sentiment, magnitude = analyze_sentiment(tweet)
        sentiments.append(sentiment)
        magnitudes.append(magnitude)

    return sentiments, magnitudes

def main():

    # Get username from user input

    username = input("Enter a Twitter username: ")
    username = "DojaCat"
    n_retrieval = int(input("Enter number of tweets to analyze: "))
    if (n_retrieval < 5 or n_retrieval > 100):
        print("Number invalid, <1 or >100")
        return

    # Retrieve unique user ID for future requests
    userID = get_userID(username)
    
    tweets_text, tweets_date = get_tweets(userID=userID, n_retrieval=n_retrieval)
        

    # Retrieve sentiment for each one of the tweets using Google NLP
    sentiments, magnitudes = get_sentiments(tweets=tweets_text)


    # Write gathered data (tweets (text contents), tweet created dates, sentiment scores, and sentiment magnitutdes) to dataframe
    df = pd.DataFrame({'text': tweets_text, 'date': tweets_date, 'sentiment': sentiments, 'magnitude': magnitudes})

    # Save to csv
    df.to_csv("./tweets.csv")
    return


if __name__ == "__main__":
    load_dotenv()
    main()