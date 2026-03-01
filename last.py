# setup

from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd

load_dotenv()
LASTFM_KEY = os.getenv('LASTFM_KEY')
LASTFM_SECRET = os.getenv('LASTFM_SECRET')

root = 'http://ws.audioscrobbler.com/2.0/'

# API GET

def get(payload):
    payload['api_key'] = LASTFM_KEY
    payload['format'] = 'json'
    return requests.get(root, params=payload)

# GET top tags

def get_top_tags(artist, track):
    
    def parse(j):
        data = j.json()
        data = pd.DataFrame(data['toptags']['tag'])
        return list(data[data['count'] >= 10]['name'])
    
    return parse(get({'method': 'track.gettoptags',
                      'artist': artist,
                      'track': track}))
    
test = get_top_tags('Joji', 'PIXELATED KISSES')
print(test)

# GET tag info

def get_tag_info(tag):

    def parse(j):
        data = j.json()
        data = pd.DataFrame(data['tag'])
        return data
    
    df = parse(get({'method': 'tag.getinfo',
                      'tag': tag})).loc['summary',]
    wiki = df[['wiki']]
    
    def parse_2(j):
        data = j.json()
        data = pd.DataFrame(data)
        print(data)

    parse_2(get({'method': 'tag.getsimilar',
                 'tag': tag}))

test = get_tag_info('rock')