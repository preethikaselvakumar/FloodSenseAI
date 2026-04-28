import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

data = [
    (1, 3.0, "Very High", "Very High", "Yes", "Low coastal zone"),
    (2, 8.0, "High", "Low", "Yes", "River influenced"),
    (3, 12.0, "High", "Low", "No", "Low-lying inland"),
    (4, 2.5, "Very High", "Very High", "Yes", "Coastal flood-prone"),
    (5, 6.0, "High", "Moderate", "No", "Urban flood-prone")
]

for row in data:
    cursor.execute("""
        INSERT INTO static_features
        (location_id, elevation_m, elevation_risk, coastal_risk, floodplain_tag, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()
conn.close()

print("Static features inserted successfully!")