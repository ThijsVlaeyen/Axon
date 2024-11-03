from datetime import datetime, timedelta

from .spotify_db import get_db_connection

def get_recent_songs_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now()
    thirty_minutes_ago = now - timedelta(minutes=600)

    cursor.execute('''
            SELECT song.song_id, song.title, song.artist, statistics.timestamp, status_name, statistics.statistic_id
            FROM statistics
            JOIN song ON song.song_id = statistics.song_id
            JOIN status ON statistics.status_id = status.status_id
            WHERE statistics.timestamp >= ?
            ORDER BY statistics.timestamp DESC
        ''', (thirty_minutes_ago,))
    
    recent_songs = cursor.fetchall()

    conn.close()
    return recent_songs

def db_update_statistic(statistic_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE statistics
            SET status_id = ?
            WHERE statistic_id = ?
        ''', (status, statistic_id))
    
    conn.commit()