import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Clear old static features
cursor.execute("DELETE FROM static_features")

# Get actual location ids from database
locations = cursor.execute("SELECT id, place FROM locations").fetchall()

for loc_id, place in locations:
    if place == "Parangipettai":
        cursor.execute("""
            INSERT INTO static_features
            (location_id, elevation_m, elevation_risk, coastal_risk, floodplain_tag, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            loc_id,
            2.0,
            "Very High",
            "Very High",
            "Yes",
            "Coastal flood-prone and surge-vulnerable area"
        ))

    elif place == "Cuddalore Town":
        cursor.execute("""
            INSERT INTO static_features
            (location_id, elevation_m, elevation_risk, coastal_risk, floodplain_tag, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            loc_id,
            5.0,
            "Very High",
            "High",
            "Yes",
            "District HQ and urban flood-prone area"
        ))

conn.commit()
conn.close()

print("✅ Static features inserted successfully!")