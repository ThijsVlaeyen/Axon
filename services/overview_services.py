import time

from .overview_models import *
from .auth_services import get_spotify_client, get_all_users, set_active_user
from .history_services import get_status

NORMAL_PLAYLIST_ID = '3GZfgYCgUg97eFYkeg7Pmm'
ULTIMATE_PLAYLIST_ID = '3sNnKMX6VhJdsDPfF4x03V' 

current_track = None
track_features = None
normal_playlist = []
ultimate_playlist = []

def get_current_song_and_check_playlists():
    global current_track
    global track_features
    if current_track and current_track['is_playing']:
        track_uri = current_track['item']['uri']
        track_id = current_track['item']['id']
        #played_count = get_played_count(track_id)
        played_count = 0

        return {
                'title': current_track['item']['name'],
                'current_song_uri': track_uri,
                'played_count': played_count,
                'song_image_url': current_track['item']['album']['images'][0]['url'],
                'normal': check_if_in_playlist(track_id, normal_playlist),
                'normal_length': len(normal_playlist),
                'ultimate': check_if_in_playlist(track_id, ultimate_playlist),
                'ultimate_length': len(ultimate_playlist),
                'normal_id': NORMAL_PLAYLIST_ID,
                'ultimate_id': ULTIMATE_PLAYLIST_ID,
                'acousticness': track_features['acousticness'],
                'danceability': track_features['danceability'],
                'energy': track_features['energy'],
                'instrumentalness': track_features['instrumentalness'],
                'liveness': track_features['liveness'],
                'loudness': track_features['loudness'],
                'speechiness': track_features['speechiness'],
                'tempo': track_features['tempo'],
                'valence': track_features['valence']
            }
    else:
        return {
            'normal_id': NORMAL_PLAYLIST_ID,
            'ultimate_id': ULTIMATE_PLAYLIST_ID
        }

def check_if_in_playlist(track_id, tracks):
    try:
        for item in tracks:
            track = item['track']
            if track and track['id'] == track_id:
                return True

        return False

    except Exception as e:
        print(f"An error occurred while checking the playlist: {e}")
        return False

def update_current_track():
    global current_track
    global track_features
    while True:
        try:
            print("Getting song...")
            users = get_all_users()
            
            for user in users:
                sp = get_spotify_client(user['name'])
                received_track = sp.current_playback()

                if received_track is not None and received_track['is_playing'] and received_track['device']['name'] == 'Kantoor':
                    set_active_user(user['name'])
                    break
            
            if received_track is None or not received_track['is_playing'] or not received_track['device']['name'] == 'Kantoor':
                time.sleep(30)
                continue

            if not current_track or received_track['item']['id'] != current_track['item']['id']:
                current_track = received_track
                track_features = sp.audio_features(current_track['item']['id'])[0]
                add_or_update_song(current_track['item']['id'], current_track['item']['name'], current_track['item']['artists'][0]['name'], get_status())
        except Exception as e:
            print(f"Error updating song: {e}")
        time.sleep(30)

def update_playlists():
    global normal_playlist
    global ultimate_playlist
    while True:
        try:
            print("Getting playlists...")
            normal_playlist = get_all_playlist_tracks(NORMAL_PLAYLIST_ID)
            ultimate_playlist = get_all_playlist_tracks(ULTIMATE_PLAYLIST_ID)
        except Exception as e:
            print(f"Error updating playlist: {e}")
        time.sleep(1800)

def get_all_playlist_tracks(playlist_id):
    tracks = []
    limit = 100
    offset = 0

    while True:
        sp = get_spotify_client('Thijs')
        response = sp.playlist_items(playlist_id = playlist_id, limit = limit, offset = offset, additional_types = ('track',))
        tracks.extend(response['items'])
        if len(response['items']) < limit:
            break

        offset += limit

    return tracks