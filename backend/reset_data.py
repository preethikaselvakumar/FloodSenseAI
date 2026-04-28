import sqlite3

conn = sqlite3.connect("../database/floodsense.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM locations")
cursor.execute("DELETE FROM static_features")
cursor.execute("DELETE FROM weather_observations")
cursor.execute("DELETE FROM predictions")

conn.commit()
conn.close()

print("Old data cleared successfully!")