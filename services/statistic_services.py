
from database import get_db_connection

def get_statistics():
    conn = get_db_connection()

    rawstats = conn.execute("""
            SELECT
                song.artist AS artist,
                song.title AS title,
                SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) AS "whistle",
                SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) AS "active",
                COUNT(s.song_id) AS "total",
                (SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) + LOG((SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1))) / (SUM(CASE WHEN s.status_id IN (1, 2) THEN 1 ELSE 0 END) + 1) AS "score"
            FROM song 
            INNER JOIN statistics s USING (song_id)
            GROUP BY song.artist, song.title
            ORDER BY score DESC
        """).fetchall()

    stats = []
    for stat in rawstats:
        stats.append({
            'artist': stat['artist'],
            'title': stat['title'],
            'whistle': stat['whistle'],
            'active': stat['active'],
            'total': stat['total'],
            'score': stat['score']
        })

    conn.close()
    return stats