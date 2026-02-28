from dotenv import load_dotenv
import hashlib

load_dotenv()

LASTFM_SIGNATURE = hashlib.md5(
    LASTFM_KEY + "xxxxxxxx" + "method" + "auth.getSession" + "token" + "xxxxxxx" + LASTFM_SECRET
)