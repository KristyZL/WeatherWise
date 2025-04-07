# Strategy Pattern: Used to allow flexible formatting of weather data (e.g., simple vs detailed output)
from api_handler import fetch_current, fetch_forecast

class WeatherStrategy:
    """
    Strategy interface for weather retrieval.
    """
    def fetch(self, location):
        pass

class CurrentWeather(WeatherStrategy):
    """
    Concrete strategy for current weather.
    """
    def fetch(self, location):
        return fetch_current(location)

class ForecastWeather(WeatherStrategy):
    """
    Concrete strategy for 5-day forecast.
    """
    def fetch(self, location):
        return fetch_forecast(location)

def get_weather(strategy, location):
    """
    Executes a given weather strategy.
    """
    return strategy.fetch(location)