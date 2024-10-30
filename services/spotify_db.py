import sqlite3

DATABASE_NAME = 'spotify.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS song (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        song_id TEXT NOT NULL,
                        title TEXT,
                        artist TEXT,
                        UNIQUE(song_id)
                    )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS status (
                        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        status_name TEXT NOT NULL
                     )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS statistics (
                        statistic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        song_id TEXT,
                        status_id INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (song_id) REFERENCES song(song_id),
                        FOREIGN KEY (status_id) REFERENCES status(status_id)
                     )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS spotify_accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        access_token TEXT,
                        refresh_token TEXT,
                        expires_at TIMESTAMP,
                        active BOOLEAN DEFAULT 0
                    )''')

        conn.commit()