from db import get_conn
from relationships.helpers import canonical_pair
import sqlite3
    
def find_relationship(userOne: int, userTwo: int) -> sqlite3.Row:
    conn = get_conn()
    pair_low, pair_high = canonical_pair(userOne, userTwo)
    try:
        cur = conn.execute(
            "SELECT * FROM friend_relationships WHERE pair_low = ? and pair_high = ?",
            (pair_low, pair_high)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()

def find_relationship_by_id(id: int) -> sqlite3.Row:
    conn = get_conn()
    try:
        cur = conn.execute(
            "SELECT * FROM friend_relationships WHERE id = ?",
            (id,)
        )
        row = cur.fetchone()
        return row
    finally:
        conn.close()

def insert_pending_relationship(sender_id: int, target_id: int) -> sqlite3.Row:
    conn = get_conn()
    pair_low, pair_high = canonical_pair(sender_id, target_id)
    try:
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
    finally:
        conn.close()