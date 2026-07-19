#!/usr/bin/env python3
# module_8_weather.py

import time
import requests

class WeatherSensor:
    def __init__(self, api_key, latitude, longitude, update_interval=300):

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.update_interval = update_interval
        self.weather_data = {}
        self.updated = False
        self.last_update = 0

    # Update Weather
    def update(self):
        now = time.time()
        self.updated = False
        if (now - self.last_update) < self.update_interval:
            return

        try:
            weather_url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?lat={self.latitude}"
                f"&lon={self.longitude}"
                f"&appid={self.api_key}"
                "&units=metric"
            )

            weather = requests.get(
                weather_url,
                timeout=10
            ).json()

            aqi_url = (
                "https://api.openweathermap.org/data/2.5/air_pollution"
                f"?lat={self.latitude}"
                f"&lon={self.longitude}"
                f"&appid={self.api_key}"
            )

            aqi = requests.get(
                aqi_url,
                timeout=10
            ).json()

            aqi_value = aqi["list"][0]["main"]["aqi"]

            levels = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor"
            }

            self.weather_data = {
                "outside_temperature": weather["main"]["temp"],
                "outside_humidity": weather["main"]["humidity"],
                "outside_pressure": weather["main"]["pressure"],
                "weather": weather["weather"][0]["main"],
                "description": weather["weather"][0]["description"],
                "wind_speed": weather["wind"]["speed"],
                "clouds": weather["clouds"]["all"],
                "aqi": aqi_value,
                "aqi_level": levels.get(aqi_value, "Unknown")
            }
            self.last_update = now
            self.updated = True

        except Exception as e:
            print("Weather API Error:", e)

    # Compatibility
    def read(self):
        self.update()
        return self.weather_data

    # Helper
    def age(self):
        if self.last_update == 0:
            return None

        return round(
            time.time() - self.last_update,
            2
        )

    # Debug
    def print_status(self):
        self.update()
        print("--------------------------------------")
        print("OUTSIDE WEATHER")
        print("--------------------------------------")

        if not self.weather_data:
            print("Waiting for API...")
            return

        data = self.weather_data

        print(f"Temperature : {data['outside_temperature']} °C")
        print(f"Humidity    : {data['outside_humidity']} %")
        print(f"Pressure    : {data['outside_pressure']} hPa")
        print(f"Weather     : {data['weather']}")
        print(f"Description : {data['description']}")
        print(f"Wind Speed  : {data['wind_speed']} m/s")
        print(f"Clouds      : {data['clouds']} %")
        print(f"AQI         : {data['aqi']}")
        print(f"AQI Level   : {data['aqi_level']}")
        print(f"Updated     : {self.updated}")
        print(f"Age         : {self.age()} sec")

def main():
    weather = WeatherSensor(
        api_key="458d5eaa4b0c933c08360cfe5c243d48",
        latitude=28.7373,
        longitude=77.0910,
        update_interval=60
    )

    while True:
        weather.update()
        weather.print_status()
        time.sleep(5)

if __name__ == "__main__":
    main()