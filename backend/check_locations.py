import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("locations:", cursor.execute("SELECT COUNT(*) FROM locations").fetchone()[0])
print("static_features:", cursor.execute("SELECT COUNT(*) FROM static_features").fetchone()[0])
print("predictions:", cursor.execute("SELECT COUNT(*) FROM predictions").fetchone()[0])

print("\nlocations rows:")
for row in cursor.execute("SELECT * FROM locations").fetchall():
    print(row)

print("\nstatic_features rows:")
for row in cursor.execute("SELECT * FROM static_features").fetchall():
    print(row)

cursor.execute("DELETE FROM locations")
conn.close()