from datetime import datetime
from .spotify_db import get_db_connection

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