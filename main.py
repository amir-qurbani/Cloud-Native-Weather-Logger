from WeatherTimerFunction.WeatherManager import WeatherManager
import os
from dotenv import load_dotenv


def main():
    # Load settings
    load_dotenv()
    # Kolla att namnet matchar din .env
    api_key = os.getenv("OPENWEATHER_API_KEY")
    conn_str = os.getenv("AZURE_CONNECTION_STRING")

    # 2. Initiera med båda nycklarna
    weather_app = WeatherManager(api_key, conn_str)

    # Här kan du behålla din logik för default city
    # (Se till att dessa metoder finns kvar i WeatherManager.py bara!)

    while True:
        print("\n--- WELCOME TO WEATHER LOGGER ---")
        print("1. Check city weather")
        print("2. View history")
        print("3. Exit")  # Jag kortade ner för exemplet, behåll dina 5 om du vill!

        choice = input("\nSelect an option (1-3): ")

        match choice:
            case "1":
                city = input("Enter the name of the city: ")
                result = weather_app.get_weather(city)

                if result:
                    weather_app.display_weather(result)
                    # 3. Ändrat metodnamn till save_to_azure
                    # Denna sköter nu AUTOMATISKT backup till SQLite om Azure är nere!
                    weather_app.save_to_azure(result)
                    print("Process complete (Saved to Cloud or Local Backup).")

            case "2":
                print("\n--- SEARCH HISTORY ---")
                weather_app.show_history()

            case "3":
                print("Goodbye!")
                break


if __name__ == "__main__":
    main()
