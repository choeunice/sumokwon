from dotenv import load_dotenv
import os
import requests

load_dotenv()
LASTFM_KEY = os.getenv('LASTFM_KEY')
LASTFM_SECRET = os.getenv('LASTFM_SECRET')
print('hi')