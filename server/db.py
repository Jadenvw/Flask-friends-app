import sqlite3
from pathlib import Path
import logging
from flask import g

logger = logging.getLogger(__name__)

# Path(file).resolve() : turns it into an absolute path object and .parent moves up one level to folder containin db.py
BASE_DIR = Path(__file__).resolve().parent # Users/Jaden/projects/labs/friends/server/app.db
DB_PATH = BASE_DIR / "app.db"

def _create_conn() -> sqlite3.Connection:
    """
    - Open a connection
    - Configure connection
        - rows to behave like dictionarie
        - foreign keys enforced
    - return connection
    * Used outside of request context
    """
    conn = sqlite3.connect(DB_PATH) # sqlite3 is an object with a connect method 
    logger.info(f"DB_PATH resolved to: {DB_PATH} (exists={DB_PATH.exists()})")
    logger.info(f"sqlite database_list: {conn.execute('PRAGMA database_list;').fetchall()}")
    logger.info("Starting DB connection")
    conn.row_factory = sqlite3.Row # adjust sqlite3 attribute to enforce wrapping each row in a Row object instead of a tuple
    # sqlite does not enfore foiegn keys automatically
    conn.execute("PRAGMA foreign_keys = ON;") # 
    return conn

def get_db() -> sqlite3.Connection:
    """
    Uses g for requests as a request-scoped storage object for db connection
    """
    if "db" not in g:
        g.db = _create_conn()
    return g.db

def close_db(e=None):
    """
    Tear down hook for db in g
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()
        logger.info("DB connection closed") 

def init_db():
    schema_path = BASE_DIR / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    conn = _create_conn()
    try:
        logger.info("Applying schema")
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
        logger.info("DB connection closed")

if __name__ == "__main__":
    init_db()
