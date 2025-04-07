from abc import ABC, abstractmethod
from api_handler import fetch_current, fetch_forecast

class WeatherStrategyBase(ABC):
    """
    Strategy interface for weather retrieval.
    """
    @abstractmethod
    def fetch(self, location):
        pass

class CurrentWeather(WeatherStrategyBase):
    """
    Concrete strategy for current weather.
    """
    def fetch(self, location):
        return fetch_current(location)

class ForecastWeather(WeatherStrategyBase):
    """
    Concrete strategy for 5-day forecast.
    """
    def fetch(self, location):
        return fetch_forecast(location)

def get_weather(strategy: WeatherStrategyBase, location):
    """
    Executes a given weather strategy.
    """
    return strategy.fetch(location)