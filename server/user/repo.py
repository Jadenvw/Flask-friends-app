"""
User Repository Layer:
    - This module is responsible strictly for data access related to the `users` table.
    - This layer must remain database-focused and side-effect free outside of executing SQL statements.

Responsibilities:
    - Execute SQL queries.
    - Return raw database rows (sqlite3.Row).
    - Perform no business logic.
    - Perform no transaction management.
    - Never call commit() or rollback().

Connection Management:
    - Uses request-scoped connection via `get_db()`.
    - Assumes transaction boundaries are handled by the service layer.
"""

# user/repo.py
import sqlite3
from db import get_db


def insert_user(username: str, password_hash: str) -> sqlite3.Row:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

    user_id = cur.lastrowid
    cur = conn.execute(
        "SELECT id, username FROM users WHERE id = ?",
        (user_id,)
    )
    return cur.fetchone()

def remove_user(user_id: int) -> None:
    conn = get_db()
    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    conn = get_db()
    cur = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
    return cur.fetchone()

def get_user_by_username(username: str) -> sqlite3.Row | None:
    conn = get_db()
    cur = conn.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )
    return cur.fetchone()
