# setup

from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
import re

load_dotenv()
LASTFM_KEY = os.getenv('LASTFM_KEY')
LASTFM_SECRET = os.getenv('LASTFM_SECRET')

root = 'http://ws.audioscrobbler.com/2.0/'

# API GET

def get(payload):
    payload['api_key'] = LASTFM_KEY
    payload['format'] = 'json'
    payload['autocorrect'] = 1
    return requests.get(root, params=payload)

# GET top tags

def get_top_tags(tuple):
    
    def parse(j):
        data = j.json()
        if 'error' in data.keys():
            raise Exception
        else:
            data = pd.DataFrame(data['toptags']['tag'])
            if len(data) == 0:
                return []
            else:
                return list(data[data['count'] >= 10]['name'])

    try:
        df = parse(get({'method': 'track.gettoptags',
                        'artist': tuple[0],
                        'track': tuple[1]}))
        return df
    except:
        try:
            correction = get({'method': 'track.getcorrection',
                              'artist': tuple[0],
                              'track': tuple[1]})
            correction = correction.json()
            if 'error' in correction.keys():
                raise Exception
        except:
            return []

# print(get_top_tags(('Joji', 'PIXELATED KISSES')))
# print(get_top_tags(('PureSnow', "I'm Never Looking Back")))

# GET tag info

def get_tag_info(tag):

    def parse(j):
        data = j.json()
        data = pd.DataFrame(data['tag'])
        return data
    
    df = parse(get({'method': 'tag.getinfo',
                      'tag': tag})).loc['summary',]
    wiki = df[['wiki']].iloc[0]
    wiki = re.split(' <a', wiki)[0]
    wiki = re.sub('\n+', ' ', wiki)
    return (tag, wiki)

# print(get_tag_info('rage'))
# print(get_tag_info('cloud rap'))

# combine top tags and tag info

def collect_tags(L):
    tags = [get_top_tags(L[i]) for i in range(0, len(L))]
    return tags

L = [('Feng', 'Cali Crazy'), ('PureSnow', "I'm Never Looking Back"), ('Saam Sultan', 'Jump Shot')]
print(collect_tags(L))

print(get_top_tags(('Feng', 'Cali Crazy')))

print(collect_tags(L[0]))