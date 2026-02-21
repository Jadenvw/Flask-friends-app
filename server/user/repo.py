from db import get_conn

def insert_user_row(username: str, password_hash: str) -> dict:
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

def delete(id: int) -> dict:
    conn = get_conn()
    try:
        conn.execute(
            "DELETE FROM users WHERE id = ?",
            (id,)
        )
        conn.commit()
        return {"message": "User Deleted"}
    finally:
        conn.close()

def get_user_by_id(id: int) -> dict:
    conn = get_conn()
    try:
        cur = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (id,)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()
