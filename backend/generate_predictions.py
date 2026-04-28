import sqlite3
import os
from datetime import datetime

# Fix DB path (important)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create predictions table
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

# Get data from both tables
rows = cursor.execute("""
SELECT l.id, l.place, l.severity, l.type, s.elevation_risk
FROM locations l
JOIN static_features s ON l.id = s.location_id
""").fetchall()

# Score mappings
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

# Loop through each location
for row in rows:
    location_id, place, severity, loc_type, elevation_risk = row

    score = (
        get_score(severity, severity_map) +
        get_score(elevation_risk, elevation_map) +
        get_score(loc_type, type_map)
    )

    # Risk classification
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

# Clear old data
cursor.execute("DELETE FROM predictions")

# Then insert new predictions

conn.commit()
conn.close()

print("✅ Predictions generated!")