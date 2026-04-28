import sqlite3

conn = sqlite3.connect("../database/floodsense.db")
cursor = conn.cursor()

rows = cursor.execute("PRAGMA table_info(weather_observations)").fetchall()

for row in rows:
    print(row)

conn.close()