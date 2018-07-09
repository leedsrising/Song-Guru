# -*- coding: utf-8 -*-

import config
import spotipy
import datetime
import spotipy.util as util
import spotipy

# getting token and creating spotify object based on [SPOTIFY_CLIENT_ID] and [SPOTIFY_CLIENT_SECRET]
token =util.oauth2.SpotifyClientCredentials(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET)
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

#the ids of the tracks to be added to the playlist
tids = []
track_list = []
for track in best_songs:
    results = spotify.search(q=track,limit = 1)
    for i, t in enumerate(results['tracks']['items']):
        tids.append(t['uri'])

#creates user playlist
now = datetime.datetime.now()
now = str(now)
scope = 'playlist-modify'
token = util.prompt_for_user_token(
    config.SPOTIFY_USERNAME,scope,
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET,
    redirect_uri=config.SPOTIFY_REDIRECT_URI)
if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist_create(SPOTIFY_USERNAME, name=now, public=True)
else:
    print "Can't get token for", SPOTIFY_USERNAME

scope = 'playlist-modify'
token = util.prompt_for_user_token(SPOTIFY_USERNAME,scope,client_id="SPOTIFY_CLIENT_ID",client_secret="8e0a4bbeb59b4822bd69ab85a6209c13",redirect_uri='https://musicrecommendation.com/callback')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_playlists(limit=50)
    #get the uri most recently created playlist
    first_playlist = (results['items'])[0]
    playlist_uri = first_playlist['uri']
else:
    print("Can't get token for", SPOTIFY_USERNAME)
