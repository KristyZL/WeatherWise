from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()  # Load environment variables

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = "{ODBC Driver 18 for SQL Server}"  # Ensure the driver is specified

try:
    # Establish connection with timeout
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Connection Timeout=30'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Get user input for a specific location
    location = input("Enter location to search: ")

    # Securely execute parameterized query
    cursor.execute("SELECT * FROM SearchHistory WHERE Location = ?", (location,))
    rows = cursor.fetchall()

    # Display results
    print("Search History:")
    if not rows:
        print("No results found.")
    else:
        for row in rows:
            print(f"ID: {row.ID}, Location: {row.Location}, Search Date: {row.SearchDate}")

except pyodbc.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()
        