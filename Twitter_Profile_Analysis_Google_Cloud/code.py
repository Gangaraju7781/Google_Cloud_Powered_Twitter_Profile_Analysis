# -*- coding: utf-8 -*-

# the above line is used to specify the type of coding.


#Importing the Lib's

import tweepy
import re
import os

#Attaching the json file which contains the credentials to acces google API's.

credential_path = r'/home/mcaleb/key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

#Importing the Lib's 

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from datetime import datetime, timedelta
from google.cloud import translate


#keys to access twitter Api: replace them with your credential's

ACC_TOKEN = '**********************************************'
ACC_SECRET = '*********************************************'
CONS_KEY = '*************************************************'
CONS_SECRET = '***********************************************'

#function to verify the api keys

def authentication(cons_key, cons_secret, acc_token, acc_secret):
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)
    return api

#function which searches the specified number of tweets by taking the user Id 

def search_tweets(userID, total_tweets):
    api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
    search_result = api.user_timeline(screen_name=userID, 
                           # 200 is the maximum allowed count
                           count=total_tweets,
                           include_rts = False,
                           )
    return search_result

#Function to clean tweets: such as removing links and usernames from the tweet

def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    clean_tweet = number_removed
    return clean_tweet

#Function for sentiment score for a tweet 

def get_sentiment_score(tweet):
    client = language.LanguageServiceClient()
    document = types\
               .Document(content=tweet,
                         type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score
    return sentiment_score

#Functon to translate the tweet to english and prints the translated text

def sample_translate_text(text, target_language, project_id):
    client = translate.TranslationServiceClient()
    contents = [text]
    parent = client.location_path(project_id, "global")
    response = client.translate_text(
        parent=parent,
        contents=contents,
        mime_type='text/plain',  
        #source_language_code='en-US',
        target_language_code=target_language)
    for translation in response.translations:
        h=translation.translated_text
        h.encode('utf-8')
        print(h.encode('utf-8'))
        return h.encode('utf-8')

#Function to analyze the tweet

def analyze_tweets(userID, total_tweets):
    score = 0
    tweets = search_tweets(userID,total_tweets)
    for tweet in tweets:
        print(tweet.text.encode('utf-8'))    
        text=tweet.text.encode('utf-8')
        target_language = 'en'
        project_id = 'project-2-327300'
        tweet1=sample_translate_text(text, target_language, project_id)
    
        cleaned_tweet = clean_tweets(tweet1)
        sentiment_score = get_sentiment_score(cleaned_tweet)
        score += sentiment_score
        print('Tweet: {}'.format(cleaned_tweet))
        print('Score: {}\n'.format(sentiment_score))
    final_score = round((score / float(total_tweets)),2)
    
    return final_score


#main function


if __name__ == '__main__':
    userID=input('enter the userID')
    total_tweets=input('tweets between 20-200')
    b=analyze_tweets(userID,total_tweets)
    print('the final score of this person is',b)
    b=float(b)
    if b <= -0.25:
        print("red zone")
    elif b>0.25 and b<= 0.25:
        print("ok")
    else:
        print("good")