import requests
import logging
from datetime import datetime
from collections import defaultdict
from config import weather_api_key
from logger import Logger
logger = Logger().get_logger()

def fetch_current(location):
    """
    Fetches current weather data from OpenWeatherMap API for a location.
    """
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": weather_api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            description = data["weather"][0]["description"]

            print(f"\nCurrent Weather for {location}:")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Description: {description.capitalize()}")

            return (location, temperature, humidity, wind_speed, description, datetime.now())

        else:
            logging.error(f"API error: {data.get('message', 'Unknown error')}")
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        print("Failed to connect to the weather service.")
        return None

def fetch_forecast(location):
    """
    Fetches 5-day forecast weather data from OpenWeatherMap API for a location.
    """
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": location,
            "appid": weather_api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            daily_forecasts = defaultdict(dict)
            for entry in data["list"]:
                dt = datetime.fromtimestamp(entry["dt"])
                date_only = dt.date()
                daily_forecasts[date_only] = entry  # always keeps the latest entry per day

            print(f"\n5-Day Forecast for {location}:")
            for date in sorted(daily_forecasts.keys())[:5]:  # limit to 5 days
                entry = daily_forecasts[date]
                dt = datetime.fromtimestamp(entry["dt"])
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                print(f"{dt}: {temp}°C, {desc.capitalize()}")
            return None  # Forecast doesn't need to be saved
        else:
            logging.error(f"API error: {data.get('message', 'Unknown error')}")
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        print("Failed to connect to the weather service.")
        return None