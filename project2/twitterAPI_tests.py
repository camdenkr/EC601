'''
Python tests to interact with the Twitter API.

By: Camden Kronhaus
Credit to: https://tinyurl.com/4s6s3xff
'''


import requests
import os
from dotenv import load_dotenv
import json

from requests.api import head
# import pandas as pd

'''
Returns the twitter unique user id associated with a username.
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
    return response.json()["data"]["id"]

'''
Returns a json of a user's Tweets. The user is specified by user_id which can be gathered from a username using
get_userID(). By default retrieves the [max_number] (default of 10) most recent tweets
'''
def get_user_tweets(user_id, start_time=None, end_time=None, max_results=10, next_token=None):
    assert (max_results<=100)

    url = "https://api.twitter.com/2/users/" + user_id + "/tweets"
    

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }
    
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'next_token': next_token
    }
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


'''
Searches through last 7 days worth of tweets with query parameter.
'''
def search_tweets(query, start_time=None, end_time=None, max_results=10, next_token=None):
    assert (max_results<=100)
    if (query == ""):
        return
    
    url = "https://api.twitter.com/2/tweets/search/recent"

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }

    
    params = {
        'query': query,
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'next_token': next_token
    }
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()  

'''
Returns all the tweets liked by a user specified by the userID, which can be gathered from the username using
get_userID()
'''
def get_liked_tweets(user_id, start_time=None, end_time=None, max_results=10, next_token=None):
    assert (max_results<=100)
    if (user_id == ""):
        return
    
    url = "https://api.twitter.com/2/users/" + user_id + "/liked_tweets"

    headers = {
        "Authorization": "Bearer " + str(os.getenv('BEARER_TOKEN'))
    }

    
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'max_results': max_results,
        'next_token': next_token
    }
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    load_dotenv()
    userID = (get_userID("DojaCat"))
    # response = get_user_tweets(user_id=userID) # Testing with ID of barack obama
    # print(json.dumps(response, indent=4, sort_keys=True))
    # response = search_tweets(query="HelloWorld") # Testing search with query
    # print(json.dumps(response, indent=4, sort_keys=True))
    response = get_liked_tweets(user_id=userID) # Testing with ID of barack obama
    print(json.dumps(response, indent=4, sort_keys=True))
if __name__ == "__main__":
    main()