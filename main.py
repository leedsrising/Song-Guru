import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import re
import copy
import operator
import spotipy
import sys
import spotipy.util as util
import datetime
import json
import config

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

# Create an extractor object:
extractor = twitter_setup()

# Creating hillydilly tweet list
hillydilly_tweets = extractor.user_timeline(screen_name="hillydilly", count=200, include_rts = False, tweet_mode = "extended")

#expanding the accepted string length so that tweets will not be truncated
pd.set_option('max_colwidth',1000)

# creating a pandas dataframe
tweetdata = []
for tweet in hillydilly_tweets:
    tweetdata.append(tweet.full_text)
hillydilly_data = pd.DataFrame(tweetdata, columns=['Tweets'])
hillydilly_data['Likes']  = np.array([tweet.favorite_count for tweet in hillydilly_tweets])
hillydilly_data['RTs']    = np.array([tweet.retweet_count for tweet in hillydilly_tweets])
hillydilly_data['General_sentiment'] = hillydilly_data['Likes'] + hillydilly_data['RTs']

def match_quotes(text):  
    matches = re.findall(r'\"(.+?)\"', text)
    if len(matches) > 0:
        return matches[0]
    raise ValueError("no matches")

def match_quotes_with_dash(text):
    matches = re.findall(r'\"(.+?)\"', text)
    if len(matches) > 0:
        artist_and_song = matches[0]
        song_start_index = artist_and_song.find("-") + 2
        return (artist_and_song[song_start_index:])
    raise ValueError("no matches")
#dashes test
#print(match_quotes_with_dash('asddsa "asdsda - duality" asddas '))
song_dictionary = {}    
    
def add_songs_to_dic(song_dictionary, tweet_dataframe, quote_type):
    for i, row in (tweet_dataframe).iterrows():
        tweet = (row["Tweets"])
        print(tweet)
        try: 
            if quote_type == "standard":
                quoted_words = match_quotes(tweet)
            elif quote_type == "dashes":
                quoted_words = match_quotes_with_dash(tweet)
            else:
                raise ValueError("quote_type")
            print(quoted_words)
            # add the song to the song dictionary
            # if the song is already in the dictionary, give it a +1 occurrence
            if quoted_words in song_dictionary:
                song_dictionary[quoted_words][0] = (song_dictionary[quoted_words])[0] + 1
            else:
                song_dictionary[quoted_words] = [1, (row["General_sentiment"])]
        except ValueError as err:
            print(err.args)

add_songs_to_dic(song_dictionary, hillydilly_data, "standard") 
