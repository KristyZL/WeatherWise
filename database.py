import pyodbc

# Database connection details (hardcoded credentials)
server = 'weatherwise-server.database.windows.net'  # Azure SQL Server name
database = 'WeatherWiseDB'  # Database name
username = 'milestone2'  # Database username
password = 'Mcmaster123'  # Database password
driver = '{ODBC Driver 18 for SQL Server}'  # ODBC driver for SQL Server

try:
    # Establish connection
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Insert a sample record
    location = 'New York'
    search_date = '2023-10-01'
    cursor.execute("INSERT INTO SearchHistory (Location, SearchDate) VALUES (?, ?)", location, search_date)
    conn.commit()
    print("Data inserted successfully!")
except pyodbc.Error as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()