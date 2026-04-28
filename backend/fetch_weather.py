import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
# Correct DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "floodsense.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all locations
locations = cursor.execute(
    "SELECT id, place, latitude, longitude FROM locations"
).fetchall()

for location in locations:
    location_id, place, lat, lon = location

    url = f"http://api.openweathermap.org/data/2.5/weather?q=Cuddalore&appid={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        # Handle API error
        if response.status_code != 200:
            print(f"Error fetching {place}: {data}")
            continue

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]

        rain_1h = 0
        if "rain" in data and "1h" in data["rain"]:
            rain_1h = data["rain"]["1h"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO weather_observations
            (location_id, timestamp, temperature, humidity, rain_1h, weather_main, weather_description, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            location_id,
            timestamp,
            temperature,
            humidity,
            rain_1h,
            weather_main,
            description,
            "OpenWeather"
        ))

        print(f"✅ Saved weather for {place}")

    except Exception as e:
        print(f"❌ Error processing {place}: {e}")

conn.commit()
conn.close()

print("🎉 All weather data saved successfully!")