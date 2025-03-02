from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
try:
    # Establish connection with timeout
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Connection Timeout=30'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Retrieve and display all records
    cursor.execute("SELECT * FROM SearchHistory")
    rows = cursor.fetchall()
    print("Search History:")
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