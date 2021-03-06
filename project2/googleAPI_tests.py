'''
Exercising Google Cloud NLP API for sentiment analysis 

Credentials located at ./google_credentials.json
Interpreting results: https://tinyurl.com/dh2t57da
API Documentation: https://tinyurl.com/e5a394w6
'''

import os
from google.cloud import language_v1
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

'''
Sentiment analysis of a string. Scale goes from -1.0 (negative) to 1.0 (positive), with 0 being neutral
'''
def sample_analyze_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

# Positive text sentiment analysis
sample_analyze_sentiment("I love dogs.")
# Negative text sentiment analysis
sample_analyze_sentiment("I hate spiders")
# Neutral text sentiment analysis
sample_analyze_sentiment("What time are we leaving?")
# Multi sentence example
sample_analyze_sentiment("I love dogs. I hate spiders. What time are we leaving?")
