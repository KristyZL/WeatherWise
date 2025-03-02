from dotenv import load_dotenv
import os
import time
import pyodbc
import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()  # Load environment variables

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"

max_retries = 3
conn = None  # Define connection variable

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

if conn is None:  # If connection failed after all attempts
    print("Failed to connect after multiple attempts.")
    logging.error("Database connection failed after multiple attempts.")
    exit()

cursor = conn.cursor()

# Get user input for a specific location
location = input("Enter location to search: ")

try:
    #  Securely execute parameterized query with logging
    cursor.execute("SELECT * FROM SearchHistory WHERE Location = ?", (location,))
    rows = cursor.fetchall()

    print("Search History:")
    if not rows:
        print("No results found.")
    else:
        for row in rows:
            print(f"ID: {row.ID}, Location: {row.Location}, Search Date: {row.SearchDate}")

except pyodbc.Error as e:
    logging.error(f"Database query error: {e}")
    print("An error occurred while accessing the database. Check logs for details.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print(f"An unexpected error occurred: {e}")
finally:
    #  Close the connection
    if conn:
        conn.close()