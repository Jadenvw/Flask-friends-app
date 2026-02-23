import sqlite3


def insert_user(conn: sqlite3.Connection, username: str, password_hash: str) -> sqlite3.Row:
    """
    1) open connect with persistance 
    2) run an INSERT into users
    3) commit
    4) close connection
    5) return the inserted user (id + username)
    """ 
    cur = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()

    id = cur.lastrowid
    cur = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    )
    row = cur.fetchone()
    return row

def remove_user(conn: sqlite3.Connection, id: int) -> None:
    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (id,)
    )
    conn.commit()

def get_user_by_id(conn: sqlite3.Connection, id: int) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    )
    row = cur.fetchone()
    return row

def get_user_by_username(conn: sqlite3.Connection, username: str) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    return row
