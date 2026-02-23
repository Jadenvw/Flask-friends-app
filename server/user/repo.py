from db import get_conn
import sqlite3

def insert_user(username: str, password_hash: str) -> sqlite3.Row:
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

        id = cur.lastrowid
        cur = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (id,)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()

def delete_user(id: int) -> sqlite3.Row:
    conn = get_conn()
    try:
        cur = conn.execute(
            "DELETE FROM users WHERE id = ?",
            (id,)
        )
        conn.commit()
        row = cur.fetchone()
        return row
    finally:
        conn.close()

def get_user_by_id(id: int) -> sqlite3.Row:
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

def get_user_by_username(username: str) -> sqlite3.Row:
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