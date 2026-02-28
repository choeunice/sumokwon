from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
LASTFM_KEY = os.getenv('LASTFM_KEY')
LASTFM_SECRET = os.getenv('LASTFM_SECRET')

root = 'http://ws.audioscrobbler.com/2.0/'

def get(payload):
    '''
    payload takes the form of key/value pair:
    'method': '...'
    '''
    payload['api_key'] = LASTFM_KEY
    payload['format'] = 'json'
    return requests.get(root, params=payload)
