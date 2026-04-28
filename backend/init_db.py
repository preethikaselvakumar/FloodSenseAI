import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place TEXT NOT NULL,
        severity TEXT,
        type TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        notes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        timestamp TEXT,
        temperature REAL,
        humidity REAL,
        rain_1h REAL,
        rain_3h REAL,
        weather_main TEXT,
        weather_description TEXT,
        source TEXT,
        FOREIGN KEY (location_id) REFERENCES locations(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS river_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        timestamp TEXT,
        river_level REAL,
        discharge REAL,
        source TEXT,
        FOREIGN KEY (location_id) REFERENCES locations(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        timestamp TEXT,
        flood_probability REAL,
        risk_level TEXT,
        confidence TEXT,
        mode TEXT,
        reason TEXT,
        FOREIGN KEY (location_id) REFERENCES locations(id)
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS static_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    elevation_m REAL,
    elevation_risk TEXT,
    coastal_risk TEXT,
    floodplain_tag TEXT,
    notes TEXT
)
""")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")