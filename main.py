import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

# Consumer credentials:
CONSUMER_KEY    = ''
CONSUMER_SECRET = ''

# Access credentials:
ACCESS_TOKEN  = ''
ACCESS_SECRET = ''

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api
    
# We create an extractor object:
extractor = twitter_setup()

# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="hillydilly", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 5 tweets:
print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print()
    
# creating a pandas dataframe
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# Displaying first 10 elements
display(data.head(10))

# We add relevant data:
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])

max_likes = 0
for likes_object in data['Likes']:
    if likes_object > max_likes:
        max_likes = likes_object
max_RTs = 0
for RT_object in data['RTs']:
    if RT_object > max_RTs:
        max_RTs = RT_object
        
return data.loc[(data['RTs'] == max_RTs)]

#returns the key of the max value of the dic
def get_min_dic_val(dic):
    min = (dic.keys())[0]
    for key in dic:
        if dic[key] > dic[min]:
            max = key
    return min

#gets 5 songs with the top "best" calculation
def get_best_songs(song_dictionary):
    sd_recalculated = {}
    for key in song_dictionary:
        (sd_recalculated[key]) = (song_dictionary[key])[0] * 7.5 + (song_dictionary[key])[1]
    print(sd_recalculated)    
    #treat "best" as sentiment + recalculated occurrences
    top5 = dict(sorted(sd_recalculated.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
    print(top5.keys())
    
get_best_songs(song_dictionary)
