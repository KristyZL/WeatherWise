# main.py

from api_handler import fetch_weather_data
from db_handler import save_weather_data, display_past_searches
import logging

def main():
    while True:
        print("\n=== WeatherWise ===")
        print("1. Get Current Weather")
        print("2. View Past Searches")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            location = input("Enter a location: ")
            data = fetch_weather_data(location)
            if data:
                save_weather_data(data)
        elif choice == '2':
            location = input("Enter location to view past data: ")
            display_past_searches(location)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    logging.info("Starting WeatherWise CLI")
    main()