from dotenv import load_dotenv
import os
import hashlib

load_dotenv()
LASTFM_KEY = os.getenv('LASTFM_KEY')
LASTFM_SECRET = os.getenv('LASTFM_SECRET')

LASTFM_SIGNATURE = hashlib.md5(
    (LASTFM_KEY + "xxxxxxxx" + "method" + "auth.getSession" +
     "token" + "xxxxxxx" + LASTFM_SECRET).encode('utf-8')).hexdigest()