import spotipy
import requests
from datetime import datetime, timedelta

from .auth_models import *

def get_all_users():
    return db_get_all_users()

def set_active_user(name):
    db_update_active_user(name)
    return

def _get_spotify_token(user_name):
    from app import app
    user = db_get_user(user_name)

    if not user:
        raise Exception(f"No user with the name {user_name} found.")

    access_token = user['access_token']
    refresh_token = user['refresh_token']
    expires_at = user['expires_at']

    if datetime.now() > datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S.%f'):
        print("Token expired, refreshing...")

        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": app.config['SPOTIPY_CLIENT_ID'],
            "client_secret": app.config['SPOTIPY_CLIENT_SECRET']
        }
        token_res = requests.post(token_url, data=token_data)
        token_json = token_res.json()

        access_token = token_json['access_token']
        expires_in = token_json['expires_in']
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        db_update_user(user_name, access_token, expires_at)

    return access_token

def get_spotify_client(user_name):
    token = _get_spotify_token(user_name)
    sp = spotipy.Spotify(auth=token)
    return sp

def callback(data):
    from app import app
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": data,
        "redirect_uri": app.config['SPOTIPY_REDIRECT_URI'],
        "client_id": app.config['SPOTIPY_CLIENT_ID'],
        "client_secret": app.config['SPOTIPY_CLIENT_SECRET'],
    }
    token_res = requests.post(token_url, data=token_data)
    token_json = token_res.json()

    # Store tokens in the database
    access_token = token_json['access_token']
    refresh_token = token_json['refresh_token']
    expires_at = datetime.now() + timedelta(seconds=token_json['expires_in'])

    conn = get_db_connection()
    conn.execute("INSERT INTO spotify_accounts (name, access_token, refresh_token, expires_at, active) VALUES (?, ?, ?, ?, ?)",
                 ('Thijs', access_token, refresh_token, expires_at, 0))
    conn.commit()
    conn.close()

def authorize_url():
    from app import app
    scope = "streaming user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private"
    return f"https://accounts.spotify.com/authorize?client_id={app.config['SPOTIPY_CLIENT_ID']}&response_type=code&redirect_uri={app.config['SPOTIPY_REDIRECT_URI']}&scope={scope}"