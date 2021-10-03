# EC601

# Project 2

## Phase 1a
**twitterAPI_tests.py** contains various functions that interact with Twitter API v2 endpoints. Tested were a function to get a user's unique id from there username (in order to easily use usernames when querying data from specific users), function to retreive a specified number of a user's tweets (to use for specific user sentiment analysis), a function to search through recent tweets based on a specific parameter, and a way to get the tweets liked by a specific user. The main function provides examples of calling each function.  

Tokens are stored in a .env file. All functions work properly when given specific users, queries, start and end times, etc. Responses are returned from functions as a json. 

## Phase 1b
**googleAPI_tests.py** contains the sample sentiment analysis from Google. Authenticates and sends a request to API to analyse the sentiment of a string. String to be provided for this project will be tweets. Main function prints out 4 examples of analysis of strings (a positive, neutral, a negative example, and a multi-sentence string). Full string score is returned as "document score" as well as the sentiment of each sentence within the string. Sentiment score ranges from -1 to +1 where -1 is negative and +1 is positive. A magnitude score is also presented to represent how much "emotional content" is in the string. A high magnitude score with a neutral score means that, as with the example in the main function, there is emotional content that "cancel" each other out and therefore provides a "mixed" sentiment. 

## Phase 2

* MVP and user stories
* Translate user stories to a modular design
* Who is your user?
* What are the basic user stories?

**social_media_analyzer.py**

### MVP and User Stories

The MVP for this project is a program that allows a user to input a twitter profile's username and be able to retrieve that user's sentiment analysis over time as a plot based on their tweets. In this way a user will be able to investigate the sentiment of the profile, or at the very least the sentiment being broadcast by the profile's tweets, and see trends over time. The user may be an average twitter user wanting to investigate public profiles, potentially that of political figures or celebrities. It may also be used by users working with thereeapists as a tool to look at their own sentiment over time.

As a patient or a therapist I want to be able to look back at my twitter feed and see how my mental health changes over time based on my mood.
As a general twitter user I want to be able to look at public figures' profiles and investigate trends in general mood for the users.

![Figure 1](/images/modular_diagram.png)
                            
                                            Figure 1: Block Diagram of modules

