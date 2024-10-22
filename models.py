from database import get_db_connection
from datetime import datetime, timedelta

def add_or_update_song(song_id, title, artist, status):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO song (song_id, title, artist)
                        VALUES (?, ?, ?)
                        ON CONFLICT(song_id) DO NOTHING''',
                    (song_id, title, artist))
        
        cur.execute('''INSERT INTO statistics (song_id, status_id, timestamp)
                        VALUES (?, ?, ?)''',
                    (song_id, status, datetime.now()))

        conn.commit()
    finally:    
        conn.close()

def get_played_count(song_id): #TODO fix
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(played_count) FROM song WHERE song_id = ?', (song_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0]

def get_recent_songs_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now()
    thirty_minutes_ago = now - timedelta(minutes=60)

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

def change_statistic(statistic_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE statistics
            SET status_id = ?
            WHERE statistic_id = ?
        ''', (status, statistic_id))
    
    conn.commit()

def get_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute()

    statistics = cursor.fetchall()

    conn.close()
    return statistics


  

