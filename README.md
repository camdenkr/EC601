# EC601

# Project 2

## Phase 1a
**twitterAPI_tests.py** contains various functions that interact with Twitter API v2 endpoints. Tested were a function to get a user's unique id from there username (in order to easily use usernames when querying data from specific users), function to retreive a specified number of a user's tweets (to use for specific user sentiment analysis), a function to search through recent tweets based on a specific parameter, and a way to get the tweets liked by a specific user. The main function provides examples of calling each function.  

Tokens are stored in a .env file. All functions work properly when given specific users, queries, start and end times, etc.

## Phase 1b
**googleAPI_tests.py** contains the sample sentiment analysis from Google. Authenticates and sends a request to API to analyse the sentiment of a string. String to be provided for this project will be tweets. Main function prints out 4 examples of analysis of strings (a positive, neutral, a negative example, and a multi-sentence string). Full string score is returned as "document score" as well as the sentiment of each sentence within the string.
