from relationships.helpers import canonical_pair
import sqlite3
    
def find_relationship(conn: sqlite3.Connection, userOne: int, userTwo: int) -> sqlite3.Row | None:
    pair_low, pair_high = canonical_pair(userOne, userTwo)
    cur = conn.execute(
        "SELECT * FROM friend_relationships WHERE pair_low = ? and pair_high = ?",
        (pair_low, pair_high)
    )
    row = cur.fetchone()
    return row

def find_relationship_by_id(conn: sqlite3.Connection, id: int) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT * FROM friend_relationships WHERE id = ?",
        (id,)
    )
    row = cur.fetchone()
    return row


def insert_pending_relationship(conn: sqlite3.Connection, sender_id: int, target_id: int) -> sqlite3.Row:
    pair_low, pair_high = canonical_pair(sender_id, target_id)
    cur = conn.execute(
        "INSERT INTO friend_relationships (pair_low, pair_high, sender_id) VALUES (?, ?, ?)",
        (pair_low, pair_high, sender_id)
    )
    conn.commit()
    
    id = cur.lastrowid
    cur = conn.execute(
        "SELECT * FROM friend_relationships WHERE id = ?",
        (id,)
    )
    row = cur.fetchone()
    return row


def update_relationship(sender_id: str, target_id: str, update: str) -> sqlite3.Row:
    pass