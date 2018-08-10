# -*- coding: utf-8 -*-

import tweepy
from IPython.display import display
import copy
import operator
import spotipy
import sys
import spotipy.util as util
import json
import config
import spotify
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import twitter

# sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon', hour=17)
# def scheduled_job():
#     print('This job is run every Monday at 5pm.')

#get_tweet_information(twitter_setup)

# authorization token for twitter using tweepy
tweepy_auth = twitter.twitter_setup()

# creating a twitter_data object
tweet_information = twitter.tweet_information(tweepy_auth)

#  turning the best_songs list of song names into a list of tids of those songs
tids = spotify.get_tids(tweet_information.best_songs)

# creating a new playlist in the user's spotify library
playlist_link = spotify.create_playlist()

# add the songs from [tids] to the newly created playlist
spotify.add_songs_to_playlist(tids)

# creates a new tweet with the playlist link
twitter.update_status(tweepy_auth, playlist_link)

