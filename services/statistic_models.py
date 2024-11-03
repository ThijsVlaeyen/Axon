from .spotify_db import get_db_connection

def db_get_statistics():
    conn = get_db_connection()

    rawstats = conn.execute("""
            SELECT
                song.artist AS artist,
                song.title AS title,
                SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) AS "whistle",
                SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) AS "active",
                COUNT(s.song_id) AS "total",
                (SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) + LOG((SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1))) / (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1) AS "score1",
                (SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) + 0.5 * LOG((SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1))) / (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1) AS "score2",
                (SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) + LOG((SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1)) * (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) / (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 2))) / (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1) AS "score3"
            FROM song 
            INNER JOIN statistics s USING (song_id)
            GROUP BY song.artist, song.title
            ORDER BY score1 DESC
        """).fetchall()
    
    conn.close()
    return rawstats

def db_get_activity():
    conn = get_db_connection()

    result = conn.execute("""
                SELECT DATE(timestamp) AS date, SUM(status_id) AS total_activity
                FROM statistics
                WHERE timestamp >= DATE('now', '-365 days') AND status_id = 1
                GROUP BY DATE(timestamp)
                ORDER BY DATE(timestamp)
        """).fetchall()

    conn.close()
    return result