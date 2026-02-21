from db import get_conn

def get_user_by_username(username):
    """
    1) Open a connection
    2) Query users table
    3) Return one row or None
    """
    conn = get_conn()
    try:
        cur = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()
