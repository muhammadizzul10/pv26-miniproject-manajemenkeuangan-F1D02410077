import sqlite3

DB_PATH = "app.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        amount INTEGER,
        category TEXT,
        type TEXT,
        priority TEXT
    )
    """)

    conn.commit()
    conn.close()