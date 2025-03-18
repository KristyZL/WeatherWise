from dotenv import load_dotenv
import os
import time
import pyodbc
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(filename="app.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()  # Load environment variables

# Database credentials
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"

# OpenWeatherMap API credentials
weather_api_key = os.getenv("WEATHER_API_KEY")
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"

max_retries = 3
conn = None  # Define connection variable

# Retry logic for database connection
for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt+1}: Connecting to the database...")
        connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Connection Timeout=30"
        conn = pyodbc.connect(connection_string, timeout=10)
        print("Connection successful!")
        break  # Exit loop if successful
    except pyodbc.Error as e:
        logging.error(f"Database connection error: {e}")
        print(f"Database error: {e}")
        time.sleep(5)  # Wait before retrying

# Exit if connection failed after multiple attempts
if conn is None:
    print("Failed to connect after multiple attempts.")
    logging.error("Database connection failed after multiple attempts.")
    exit()

cursor = conn.cursor()

# Ensure `WeatherData` table exists
try:
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='WeatherData' AND xtype='U')
        CREATE TABLE WeatherData (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            Location NVARCHAR(100) NOT NULL,
            Temperature FLOAT NOT NULL,
            Humidity INT NOT NULL,
            WindSpeed FLOAT NOT NULL,
            Description NVARCHAR(255) NOT NULL,
            SearchDate DATETIME NOT NULL
        )
    ''')
    conn.commit()
    print("Ensured WeatherData table exists.")
except pyodbc.Error as e:
    logging.error(f"Error ensuring WeatherData table exists: {e}")
    print("Error creating WeatherData table. Check logs for details.")

def fetch_weather_data(location):
    """
    Fetches weather data from OpenWeatherMap API.
    """
    try:
        params = {
            "q": location,
            "appid": weather_api_key,
            "units": "metric"  # Fetch data in Celsius
        }
        response = requests.get(weather_api_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            description = data["weather"][0]["description"]
            
            print(f"\nWeather Data for {location}:")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Description: {description.capitalize()}\n")

            return (location, temperature, humidity, wind_speed, description, datetime.now())

        else:
            print(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
            return None

    except requests.RequestException as e:
        logging.error(f"API request error: {e}")
        print("Failed to retrieve weather data. Check logs for details.")
        return None

def save_weather_data(weather_info):
    """
    Saves fetched weather data into the database.
    """
    if weather_info:
        try:
            cursor.execute('''
                INSERT INTO WeatherData (Location, Temperature, Humidity, WindSpeed, Description, SearchDate)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', weather_info)
            conn.commit()
            print("Weather data saved successfully!\n")
        except pyodbc.Error as e:
            logging.error(f"Database insert error: {e}")
            print("Failed to save weather data. Check logs for details.")

# User input for location
location = input("Enter a location to fetch weather data: ")

# Fetch and save weather data
weather_data = fetch_weather_data(location)
if weather_data:
    save_weather_data(weather_data)

# Retrieve and display past searches
try:
    cursor.execute("SELECT * FROM WeatherData WHERE Location = ?", (location,))
    rows = cursor.fetchall()

    print("Past Weather Searches:")
    if not rows:
        print("No previous records found.")
    else:
        for row in rows:
            print(f"{row.SearchDate}: {row.Location} - {row.Temperature}°C, {row.Humidity}% humidity, {row.WindSpeed}m/s, {row.Description}")

except pyodbc.Error as e:
    logging.error(f"Database query error: {e}")
    print("An error occurred while accessing the database. Check logs for details.")

# Close the database connection
finally:
    if conn:
        conn.close()