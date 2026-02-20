import sqlite3
from pathlib import Path

# Path(file).resolve() : turns it into an absolute path object and .parent moves up one level to folder containin db.py
BASE_DIR = Path(__file__).resolve().parent # Users/Jaden/projects/labs/friends/server/app.db
DB_PATH = BASE_DIR / "app.db"

def get_conn():
    """
    - Open a connection
    - Configure connection
        - rows to behave like dictionarie
        - foreign keys enforced
    - return connection
    """
    conn = sqlite3.connect(DB_PATH) # sqlite3 is an object with a connect method 
    conn.row_factory = sqlite3.Row # adjust sqlite3 attribute to enforce wrapping each row in a Row object instead of a tuple
    # sqlite does not enfore foiegn keys automatically
    conn.execute("PRAGMA foreign_keys = ON;") # 
    return conn

def init_db():
    schema_path = BASE_DIR / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = get_conn()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


