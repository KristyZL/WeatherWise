from strategies import get_weather, CurrentWeather, ForecastWeather
from db_handler import save_weather_data, display_past_searches
import logging
from logger import setup_logger

# Set up logging
setup_logger()

def main():
    while True:
        print("\n=== WeatherWise ===")
        print("1. Get Current Weather")
        print("2. View 5-Day Forecast")
        print("3. View Past Searches")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            location = input("Enter a location: ")
            # Use Strategy Pattern for current weather
            data = get_weather(CurrentWeather(), location)
            if data:
                save_weather_data(data)

        elif choice == '2':
            location = input("Enter a location: ")
            # Use Strategy Pattern for 5-day forecast
            get_weather(ForecastWeather(), location)

        elif choice == '3':
            location = input("Enter a location to view history: ")
            display_past_searches(location)

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1–4.")

if __name__ == "__main__":
    logging.info("Starting WeatherWise CLI")
    main()