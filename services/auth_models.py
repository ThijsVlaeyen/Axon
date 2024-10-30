from .spotify_db import get_db_connection

def db_get_user(user):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM spotify_accounts WHERE name = ?", (user,)).fetchone()
    conn.close()
    return user

def db_get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM spotify_accounts ORDER BY active DESC").fetchall()
    conn.close()
    return users

def db_update_active_user(name):
    conn = get_db_connection()

    conn.execute("""UPDATE spotify_accounts SET active = false""")

    conn.execute("""UPDATE spotify_accounts SET active = true WHERE name = ?"""
            , (name,))

    conn.commit()
    conn.close()
    return

def db_update_user(name, access_token, expires):
    conn = get_db_connection()

    conn.execute("""
            UPDATE spotify_accounts
            SET access_token = ?, expires_at = ?
            WHERE name = ?
        """, (access_token, expires, name))
    conn.commit()
    conn.close()
    return