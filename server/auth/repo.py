from db import get_conn

def create_user(username: str, password_hash: str) -> dict:
    """
    1) open connect with persistance 
    2) run an INSERT into users
    3) commit
    4) close connection
    5) return the inserted user (id + username)
    """
    conn = get_conn()
    try: 
        cur = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return {"id": cur.lastrowid, "username": username}
    finally:
        conn.close()


