from WeatherManager import WeatherManager
import os
from dotenv import load_dotenv


def main():
    # Load settings
    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Initialize our manager
    weather_app = WeatherManager(api_key)

    while True:
        print("\n--- WELCOME TO WEATHER LOGGER ---")
        print("1. Check city weather")
        print("2. View history")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ")

        match choice:
            case "1":
                city = input("Enter the name of the city: ")
                # 1. Get the data
                result = weather_app.get_weather(city)

                if result:
                    # 2. Show it to the user
                    weather_app.display_weather(result)
                    # 3. Save it to the database
                    weather_app.save_to_db(result)
                    print("Successfully logged to database.")

            case "2":
                print("\n--- SEARCH HISTORY ---")
                weather_app.show_history()

            case "3":
                print("Thank you for using Weather Logger. Goodbye!")
                break  # This stops the loop and exits the app

            case _:
                print("Invalid choice, please try again (1, 2 or 3).")


if __name__ == "__main__":
    main()
