import sqlite3
import requests
from datetime import datetime

API_KEY = "bc2dd0fda7728e0e614809ace68d7fdb"

conn = sqlite3.connect("../database/floodsense.db")
cursor = conn.cursor()

locations = cursor.execute("SELECT id, place, latitude, longitude FROM locations").fetchall()

for location in locations:
    location_id, place, lat, lon = location

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    forecast_data = response.json()

    list_data = forecast_data["list"][:8]  # First 8 time steps = 24 hours

    # Extract key forecast features
    next_3h_rain = list_data[0]["pop"] * list_data[0].get("rain", {}).get("3h", 0) if "pop" in list_data[0] else 0
    next_6h_rain = sum(item.get("rain", {}).get("3h", 0) for item in list_data[:2])
    next_24h_rain = sum(item.get("rain", {}).get("3h", 0) for item in list_data[:8])
    
    trend = "increasing" if next_3h_rain > list_data[0].get("rain", {}).get("3h", 0) else "decreasing"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO weather_observations 
    (location_id, timestamp, rain_forecast_3h, rain_forecast_6h, 
     rain_forecast_24h, rainfall_trend, weather_main, weather_description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    location_id,
    timestamp,
    next_3h_rain,
    next_6h_rain,
    next_24h_rain,
    trend,
    "Forecast",
    forecast_data["list"][0]["weather"][0]["description"]
))

    print(f"✅ Forecast saved for {place}: {next_3h_rain:.1f}mm 3h, trend={trend}")

conn.commit()
conn.close()

print("🎉 All forecast data saved successfully!")