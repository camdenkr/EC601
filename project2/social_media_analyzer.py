# Used to gather social media sentiment analysis for a specific Twitter user
import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from requests.api import head

import os
from google.cloud import language_v1

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"


'''
Returns the twitter unique user id associated with a username.
:param: username: a Twitter username string
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


'''
Takes in a tweet ID and identifies when it was created
'''
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
            tweets_date.append(datetime.strptime(tweet_date_lookup(tweet["id"]).split("T")[0], "%Y-%m-%d"))
            if(len(tweets_text)>=n_retrieval):
                break
    return tweets_text, tweets_date



'''
Analyzes the sentiment of a single piece of text and returns sentiment score and magnitude of it from Google NLP API
:param text_content: string, text to analyze sentiment
:return sentiment: sentiment score
:return magnitude: magnitude score
'''
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

'''
Plots data gathered from tweets.
Credit to matplotlib documentation for most of the plotting functionality: https://tinyurl.com/3cm4hxmx
:param df: dataframe of tweet data
'''
def plot_data(df):
    # Convert dates to list in datetime format
    dates = [date for date in df["date"]]

    # Covnert sentiments to a list from df
    sentiments = [float(s) for s in df["sentiment"]]
    levels = np.array(sentiments)

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Sentiment over time")

    ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(dates, np.zeros_like(dates), "o-",
            color="k", markerfacecolor="w")  # Baseline and markers on it.

    names = [str(round(s,2)) for s in sentiments]
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, names, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="right")
    # format xaxis with 4 month intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    # remove y axis and spines
    ax.yaxis.set_visible(True)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    plt.show()

    return


def main():

    # # Get username from user input

    username = input("Enter a Twitter username: ")

    # Retrieve unique user ID for future requests
    userID = get_userID(username)
    
    tweets_text, tweets_date = get_tweets(userID=userID, n_retrieval=100) # Retrieve Tweet data
    sentiments, magnitudes = get_sentiments(tweets=tweets_text) # Retrieve sentiment data

    # # Write gathered data to dataframe.
    df = pd.DataFrame({'text': tweets_text, 'date': tweets_date, 'sentiment': sentiments, 'magnitude': magnitudes})
    
    
    # Save to csv
    # df.to_csv("./tweets.csv")
    
    plot_data(df)


    
    return


if __name__ == "__main__":
    load_dotenv()
    main()