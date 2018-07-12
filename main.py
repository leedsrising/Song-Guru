# -*- coding: utf-8 -*-

import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import re
import copy
import operator
import spotipy
import sys
import spotipy.util as util
import datetime
import json
import config
import spotify

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
hillydilly_tweets = extractor.user_timeline(
    screen_name="hillydilly", 
    count=200, 
    include_rts = False, 
    tweet_mode = "extended"
    )

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
    
# adds the songs from [tweet_dataframe], a pandas dataframe containing song tweets,
# to the existing [song_dictionary] library by finding songs that are quoted under
# the format of [quote_type]
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
            # add the song to the song dictionary
            # if the song is already in the dictionary, give it a +1 occurrence
            if quoted_words in song_dictionary:
                song_dictionary[quoted_words][0] = (song_dictionary[quoted_words])[0] + 1
            else:
                song_dictionary[quoted_words] = [1, (row["General_sentiment"])]
        except ValueError as err:
            print(err.args)

add_songs_to_dic(song_dictionary, hillydilly_data, "standard") 

# returns the key of the max value of the dic
def get_min_dic_key(dic):
    min = (dic.keys())[0]
    for key in dic:
        if dic[key] < dic[min]:
            min = key
    return min

# returns dictionary of 10 best song with recalculated values based on number 
# of likes and retweets
def get_best_songs(song_dictionary):
    sd_recalculated = {} 
    for key in song_dictionary:
        (sd_recalculated[key]) = (song_dictionary[key])[0] * 7.5 + (song_dictionary[key])[1]
    # treat "best" as sentiment + recalculated occurrences
    accum = {}
    for key in sd_recalculated:
        if len(accum.keys()) < 10:
            accum[key] = sd_recalculated[key]
        else:
            min = get_min_dic_key(accum)
            if sd_recalculated[key] > accum[min]:    
                del accum[min]
                accum[key] = sd_recalculated[key]
        return accum

# creating hypemachine tweet list
hypemachine_tweets = extractor.user_timeline(
    screen_name="hypem", 
    count=200, 
    include_rts = False, 
    tweet_mode = "extended")
print("Number of tweets extracted: {}.\n".format(len(hypemachine_tweets)))

# Create a list of hypemachine tweets
tweetdata = []
for tweet in hypemachine_tweets:
    tweetdata.append(tweet.full_text)
hypemachine_data = pd.DataFrame(tweetdata, columns=['Tweets'])
hypemachine_data['Likes']  = np.array([tweet.favorite_count for tweet in hypemachine_tweets])
hypemachine_data['RTs']    = np.array([tweet.retweet_count for tweet in hypemachine_tweets])
hypemachine_data['General_sentiment'] = hypemachine_data['Likes'] + hypemachine_data['RTs']

add_songs_to_dic(song_dictionary, hypemachine_data, "standard")

# Creating submithub tweet list
submithub_tweets = extractor.user_timeline(
    screen_name="submit_hub", 
    count=1000, 
    include_rts = False, 
    tweet_mode = "extended")
print("Number of tweets extracted from submithub: {}.\n".format(len(submithub_tweets)))

# Create a list of submithub tweets
tweetdata = []
for tweet in submithub_tweets:
    tweetdata.append(tweet.full_text)
submithub_data = pd.DataFrame(tweetdata, columns=['Tweets'])
submithub_data['Likes']  = np.array([tweet.favorite_count for tweet in submithub_tweets])
submithub_data['RTs']    = np.array([tweet.retweet_count for tweet in submithub_tweets])
submithub_data['General_sentiment'] = submithub_data['Likes'] + submithub_data['RTs']

add_songs_to_dic(song_dictionary, submithub_data, "dashes")

#getting the top 5 best songs from this song dictionary
best_songs = get_best_songs(song_dictionary)
print("the best songs: " + str(best_songs))
# turning the best_songs list of song names into a list of tids of those songs
tids = spotify.get_tids(best_songs)

# creating a new playlist in the user's spotify library
spotify.create_playlist()

# add the songs from [tids] to the newly created playlist
spotify.add_songs_to_playlist(tids)

