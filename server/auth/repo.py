import sqlite3

def insert_revoked_token(conn: sqlite3.Connection, jti: str, expires_at: str | None) -> None:
    pass
 
def is_token_revoked(conn: sqlite3.Connection, jti: str) -> bool:
    pass
