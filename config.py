# config.py

# Import libraries to load environment variables
import os
from dotenv import load_dotenv

# Load variables from .env file into the system environment
load_dotenv()

# Database credentials
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# SQL Server driver
driver = "{ODBC Driver 18 for SQL Server}"

# OpenWeatherMap API key
weather_api_key = os.getenv("WEATHER_API_KEY")