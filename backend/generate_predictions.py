import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    timestamp TEXT,
    risk_score REAL,
    risk_level TEXT,
    reason TEXT
)
""")

# Clear old predictions first
cursor.execute("DELETE FROM predictions")

rows = cursor.execute("""
SELECT l.id, l.place, l.severity, l.type, s.elevation_risk
FROM locations l
JOIN static_features s ON l.id = s.location_id
""").fetchall()

severity_map = {
    "Very High": 40,
    "High": 25,
    "Moderate": 15
}

elevation_map = {
    "Very High": 30,
    "High": 20,
    "Moderate": 10
}

type_map = {
    "coastal": 15,
    "near_river": 15,
    "urban": 10
}

def get_score(value, mapping):
    return mapping.get(value, 0)

for row in rows:
    location_id, place, severity, loc_type, elevation_risk = row

    score = (
        get_score(severity, severity_map) +
        get_score(elevation_risk, elevation_map) +
        get_score(loc_type, type_map)
    )

    if score >= 60:
        level = "Danger"
    elif score >= 30:
        level = "Warning"
    else:
        level = "Safe"

    reason = f"{severity} + {elevation_risk} + {loc_type}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO predictions (location_id, timestamp, risk_score, risk_level, reason)
    VALUES (?, ?, ?, ?, ?)
    """, (location_id, timestamp, score, level, reason))

    print(f"{place} → {score} → {level}")

conn.commit()
conn.close()

print("✅ Predictions generated!")