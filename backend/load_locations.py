import sqlite3
import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")
CSV_PATH = os.path.join(BASE_DIR,"..", "locations.csv")

def load_locations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(CSV_PATH, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
                INSERT INTO locations (place, severity, type, latitude, longitude, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row['place'],
                row.get('severity', ''),
                row.get('type', ''),
                float(row['latitude']),
                float(row['longitude']),
                row.get('notes', '')
            ))

    conn.commit()
    conn.close()

    print("Locations inserted successfully!")

if __name__ == "__main__":
    load_locations()