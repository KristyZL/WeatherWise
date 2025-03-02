import pyodbc

# Database connection details (hardcoded credentials)
server = 'weatherwise-server.database.windows.net'  # Azure SQL Server name
database = 'WeatherWiseDB'  # Database name
username = 'milestone2'  # Database username
password = 'Mcmaster123'  # Database password
driver = '{ODBC Driver 18 for SQL Server}'  # ODBC driver for SQL Server

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