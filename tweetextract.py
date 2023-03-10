# -*- coding: utf-8 -*-

twitter_api_key = input("Please enter your twitter API key:") # code provided by starting template

twitter_api_key_secret = input("Please enter your twitter API key secret:") # code added as required for tweet retrieval

twitter_access_token = input("Please enter your twitter access token:") # code added as required for tweet retrieval

twitter_access_token_secret = input("Please enter your twitter access token secret:"); # code added as required for tweet retrieval

openai_api_key = input("Please enter your OpenAI API key:") # code provided by starting template

!pip install twitter
!pip install tweepy
!pip install pandas

import pandas as pd
import tweepy

def get_tweets_by_handle(handle: str, api_key: str):
  # ...your code here

  # code for twitter authentication, uses the information entered by the user in Step 1
  auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
  auth.set_access_token(twitter_access_token, twitter_access_token_secret)

  # create an api object which we'll use to retrieve the tweets
  api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) # add rate limits 

  tweets = [] # declare an array to store the tweets

  # use the API object to retrieve the latest tweets, the number of which is indicated by the "counter" parameter
  tweets = api.user_timeline(screen_name=handle, count=20) 

  #for tweet in tweets:
    #print(tweet.text)

  # extract and store only the tweet's text, the tweet ID, and user's twitter handle
  tweet_list = [[tweet.text, tweet.id, tweet.user.screen_name] for tweet in tweets] # iterate through all the tweets retrieved
  
  tweetsPandasDF = pd.DataFrame(tweet_list, columns=['text', 'tweet_id', 'handle']) # convert 
  #print(tweetsPandasDF)

  return tweetsPandasDF # an output of tweets pandas dataframe as requested by the instructions

!pip install openai

import os
import openai
import re

def check_deal_from_tweet(tweet: str, api_key: str) -> bool:

  # ... your code here

  # remove links included in tweet as they cause us to go over the token limit/threshold
  tweet = re.sub(r'https?:\/\/\S+', '', tweet) 

  openai.api_key = api_key # set the api key

  # write up a prompt for OpenAI
  prompt = (f"Does this tweet have a deal? {tweet}") # prompt includes the question and the tweet in question

  # 
  completions = openai.Completion.create(
      engine = "text-davinci-002", # ID of the model to use
      prompt = prompt, # the prompt created earlier that we are using to question OpenAI
      max_tokens = 280, # the maximum number of tokens to generate in the completion.
      n = 1, # how many completions to generate for each prompt
      stop = '.',
      temperature = 0.7, # the sampling temperature to be use. Higher values means the model will take more risks.
  )

  message = completions.choices[0].text # retrieve and store response from OpenAI

  # check message returned by OpenAI to see if it detects a deal
  if "True" in message or "Yes" in message:   # if a deal is detected to be present set boolean var to true
    dealTF = True             
  else:    # if no deal is detected to be present set boolean variable to false
    dealTF = False 

  return dealTF # return the boolean variable requested by the instructions that indicates whether a deal was detected

import json

handle = 'RedFlagDeals' # you can use any handle for testing here
output = [] # list of dictionaries declared for final output

# get tweets
tweets = get_tweets_by_handle(handle, twitter_api_key)

# 
tweet_array = tweets.values.tolist() # convert back into array from pandas dataframe

# ...your code here
# iterate over all the tweets and get predict 
val = True
for tweet in tweet_array:
  val = check_deal_from_tweet(tweet[0], openai_api_key)
  output.append({
      'handle': tweet[2],
      'tweet': tweet[0],
      'tweet_id': tweet[1],
      'hasDeal': val
  })

#output = '\n'.join(str(twt) for twt in output)

print(json.dumps(output, indent = 1, separators=(',', ': ')))
