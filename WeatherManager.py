import requests
import os
import sqlite3
from dotenv import load_dotenv


class WeatherManager:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"

            response = requests.get(url)
            data = response.json()

            # Check if the API request was successful (200 = OK)
            if data.get("cod") != 200:
                print(f"Error: Could not find city '{city}'")
                return None

            return data
        except Exception as e:
            print(f"Oops, something went wrong: {e}")
            return None

    def display_weather(self, data):
        if data:
            city_name = data["name"]
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]

            print(f"In {city_name} it is {temp} degrees and {description}.")

    def save_to_db(self, data):
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS weather_logs("
                       "id INTEGER PRIMARY KEY, city TEXT, temperature REAL, description TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

        city = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        cursor.execute(
            "INSERT INTO weather_logs (city, temperature, description) VALUES (?,?,?)", (city, temp, desc))

        connection.commit()
        connection.close()

    def show_history(self):
        try:
            connection = sqlite3.connect("my_database.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM weather_logs ORDER BY timestamp DESC LIMIT 5")
            rows = cursor.fetchall()

            if not rows:
                print("No history found.")
            else:
                print("\n--- WEATHER SEARCH HISTORY ---")
                print(
                    f"{'DATE & TIME':<20} | {'CITY':<15} | {'TEMP':<7} | {'CONDITION'}")
                print("-" * 65)

                for id, city, temp, desc, time in rows:
                    print(f"{time:<20} | {city:<15} | {temp:<7}°C | {desc}")
            connection.close()
        except Exception as e:
            print(f" Erorr reading from database {e}")

    def delete_history(self):
        try:
            connection = sqlite3.connect("my_database.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM weather_logs")

            connection.commit()
            connection.close()
            print("\n--- History has been cleard succesfully ---")
        except Exception as e:
            print(f"Error deleting history: {e}")


# Load environment variables
load_dotenv()
secret_key = os.getenv("API_KEY")

# Start the application
weather_app = WeatherManager(secret_key)
result = weather_app.get_weather("Paris")

# Display the result
weather_app.display_weather(result)
weather_app.save_to_db(result)
