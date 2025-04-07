# Repository Pattern: This class provides an abstraction over direct database access, enabling cleaner separation of concerns
import pyodbc
import logging
from config import server, database, username, password, driver
from logger import setup_logger

# Set up logging
setup_logger()

def connect_to_database():
    """
    Establish connection to the Azure SQL Database.
    """
    try:
        connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None

def save_weather_data(data):
    """
    Save the fetched weather data to the WeatherData table.
    Creates the table if it doesn't exist.
    """
    conn = connect_to_database()
    if not conn:
        print("DB connection failed.")
        return

    try:
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='WeatherData' AND xtype='U')
            CREATE TABLE WeatherData (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                Location NVARCHAR(100),
                Temperature FLOAT,
                Humidity INT,
                WindSpeed FLOAT,
                Description NVARCHAR(255),
                SearchDate DATETIME
            )
        ''')

        # Insert weather data
        cursor.execute('''
            INSERT INTO WeatherData (Location, Temperature, Humidity, WindSpeed, Description, SearchDate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)

        conn.commit()
        print("Weather data saved.")
        logging.info(f"Data saved for {data[0]}.")

    except pyodbc.Error as e:
        logging.error(f"Insert failed: {e}")
        print("Failed to save data.")
    finally:
        conn.close()

def display_past_searches(location):
    """
    Retrieve and display past weather searches for a location.
    """
    conn = connect_to_database()
    if not conn:
        print("DB connection failed.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WeatherData WHERE Location = ?", (location,))
        rows = cursor.fetchall()

        if rows:
            print(f"\nPast searches for {location}:")
            for row in rows:
                print(f"{row.SearchDate}: {row.Temperature}°C, {row.Humidity}%, {row.WindSpeed} m/s, {row.Description}")
        else:
            print("No past records found.")

    except pyodbc.Error as e:
        logging.error(f"Query failed: {e}")
        print("Failed to fetch records.")
    finally:
        conn.close()