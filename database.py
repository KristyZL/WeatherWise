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

    # Create the SearchHistory table if it doesn't exist
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SearchHistory' AND xtype='U')
        CREATE TABLE SearchHistory (
            ID INT IDENTITY(1,1) PRIMARY KEY,
            Location NVARCHAR(100) NOT NULL,
            SearchDate DATETIME NOT NULL
        )
    ''')
    conn.commit()
    print("SearchHistory table created successfully!")
except pyodbc.Error as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()