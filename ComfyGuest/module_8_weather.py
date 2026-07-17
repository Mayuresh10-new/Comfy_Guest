#!/usr/bin/env python3
# module_8_weather.py

import requests
import time


class WeatherSensor:

    def __init__(
        self,
        api_key,
        latitude,
        longitude,
        update_interval=300
    ):
        """
        Weather Sensor Module

        api_key         : OpenWeatherMap API Key
        latitude        : Latitude
        longitude       : Longitude
        update_interval : Seconds between API calls
        """

        self.api_key = api_key

        self.latitude = latitude
        self.longitude = longitude

        self.update_interval = update_interval

        self.last_update = 0

        self.weather_data = {}

    ########################################################

    def update(self):

        """
        Fetch latest weather and AQI data.
        """

        current_time = time.time()

        if current_time - self.last_update < self.update_interval:

            return self.weather_data

        try:

            ##################################################
            # Weather
            ##################################################

            weather_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={self.latitude}"
                f"&lon={self.longitude}"
                f"&appid={self.api_key}"
                f"&units=metric"
            )

            weather = requests.get(weather_url, timeout=10).json()

            ##################################################
            # AQI
            ##################################################

            aqi_url = (
                f"https://api.openweathermap.org/data/2.5/air_pollution"
                f"?lat={self.latitude}"
                f"&lon={self.longitude}"
                f"&appid={self.api_key}"
            )

            aqi = requests.get(aqi_url, timeout=10).json()

            ##################################################

            aqi_value = aqi["list"][0]["main"]["aqi"]

            ##################################################

            levels = {

                1: "Good",

                2: "Fair",

                3: "Moderate",

                4: "Poor",

                5: "Very Poor"

            }

            ##################################################

            self.weather_data = {

                "outside_temperature":
                    weather["main"]["temp"],

                "outside_humidity":
                    weather["main"]["humidity"],

                "outside_pressure":
                    weather["main"]["pressure"],

                "weather":
                    weather["weather"][0]["main"],

                "description":
                    weather["weather"][0]["description"],

                "wind_speed":
                    weather["wind"]["speed"],

                "clouds":
                    weather["clouds"]["all"],

                "aqi":
                    aqi_value,

                "aqi_level":
                    levels.get(aqi_value, "Unknown")

            }

            self.last_update = current_time

        except Exception as e:

            print("Weather API Error:", e)

        return self.weather_data

    ########################################################

    def read(self):

        return self.update()

    ########################################################

    def print_status(self):

        data = self.update()

        print("--------------------------------------")
        print("OUTSIDE WEATHER")
        print("--------------------------------------")

        if not data:

            print("Waiting for API...")

            return

        print("Temperature :", data["outside_temperature"], "°C")
        print("Humidity    :", data["outside_humidity"], "%")
        print("Pressure    :", data["outside_pressure"], "hPa")
        print("Weather     :", data["weather"])
        print("Description :", data["description"])
        print("Wind Speed  :", data["wind_speed"], "m/s")
        print("Clouds      :", data["clouds"], "%")
        print("AQI         :", data["aqi"])
        print("AQI Level   :", data["aqi_level"])


############################################################

def main():

    weather = WeatherSensor(

        api_key="458d5eaa4b0c933c08360cfe5c243d48",

        latitude=28.7373,

        longitude=77.0910,

        update_interval=60

    )

    print("Reading Weather...")

    while True:

        weather.print_status()

        time.sleep(5)


############################################################

if __name__ == "__main__":

    main()