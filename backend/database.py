import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "cyber_framework.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    # Devices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (

            device_id TEXT PRIMARY KEY,

            platform TEXT NOT NULL,

            role TEXT NOT NULL,

            status TEXT NOT NULL,

            registered_at TEXT NOT NULL,

            last_seen TEXT NOT NULL
        )
    """)

    # Security events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (

            event_id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            event_type TEXT NOT NULL,

            source TEXT NOT NULL,

            target TEXT,

            severity TEXT NOT NULL,

            message TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()