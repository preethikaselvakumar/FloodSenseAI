# Add to backend/add_forecast_columns.py
import sqlite3

conn = sqlite3.connect("../database/floodsense.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE weather_observations ADD COLUMN rain_forecast_3h REAL")
cursor.execute("ALTER TABLE weather_observations ADD COLUMN rain_forecast_6h REAL")
cursor.execute("ALTER TABLE weather_observations ADD COLUMN rain_forecast_24h REAL")
cursor.execute("ALTER TABLE weather_observations ADD COLUMN rainfall_trend TEXT")

conn.commit()
conn.close()

print("Forecast columns added!")