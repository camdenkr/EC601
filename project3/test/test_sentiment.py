import pytest

# Must set up credentials with the following or using CI
import os
from dotenv import load_dotenv
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials"
load_dotenv()

from ..social_media_analyzer import *


def test_analyze_sentiment_good():
    assert(round(analyze_sentiment("Very good. I am Very happy.")[0]) == 1 ) # Positive Sentiment
    return

def test_analyze_sentiment_bad():
    assert(round(analyze_sentiment("I am unsure. I am alright.")[0]) == 0) # Neutral Sentiment
    return


def test_analyze_sentiment_neutral():
    assert(round(analyze_sentiment("Very bad. I am very Sad")[0]) == -1) # Negative Sentiment
    return
