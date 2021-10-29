import pytest

import os
from dotenv import load_dotenv
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"
load_dotenv()

from ..social_media_analyzer import *

# Assert retrieves correct User ID of DojaCat
def test_get_userID():
    #DojaCat ID known to be:
    uid = get_userID("DojaCat")
    assert(uid == "568545739") 

# Tests tweets and be retrieved correctly
def test_get_tweets():
    tweets_text, tweets_date = get_tweets(userID="568545739",n_retrieval=10)
    assert(len(tweets_text) == len(tweets_date) == 11) # Assert shape of return values is = n_retrieval

# Assert tweet_date_lookup retrieves correctly from known tweet: https://twitter.com/BarackObama/status/1441417526890536967
def test_tweet_date_lookup():
    assert(tweet_date_lookup("1441417526890536967") == "2021-09-24T15:01:33.000Z")