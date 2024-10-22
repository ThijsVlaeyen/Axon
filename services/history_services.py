from datetime import datetime

def get_recent_songs():
    from models import get_recent_songs_db
    from .overview_services import check_if_in_playlist, normal_playlist, ultimate_playlist
    
    recent_songs = get_recent_songs_db()
    return [
        {
            "song_id": song_id,
            "statistics_id": statistic_id,
            "title": title,
            "artist": artist,
            "timestamp": datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S'),
            "status_name": status_name,
            "in_normal_playlist": check_if_in_playlist(song_id, normal_playlist),
            "in_ultimate_playlist": check_if_in_playlist(song_id, ultimate_playlist)
        }
        for song_id, title, artist, timestamp, status_name, statistic_id in recent_songs
    ]

status = 2
def set_status(stat):
    global status
    status = stat

def get_status():
    global status
    return status