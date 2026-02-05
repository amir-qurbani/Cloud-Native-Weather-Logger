import requests
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


class WeatherManager:

    def __init__(self, api_key):
        self.api_key = api_key
        self.conn_str = os.getenv("AZURE_CONNECTION_STRING")

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
        """ connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS WeatherData("
                       "id INTEGER PRIMARY KEY, city TEXT, temperature REAL, description TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS setting (name TEXT PRIMARY KEY, value TEXT)") """
        try:
            city = data["name"]
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO WeatherData (city, temperature, description) VALUES (?,?,?)", (city, temp, desc))

            conn.commit()
            conn.close()
            print(f"✅ Sparat i Azure: {city}")
        except Exception as e:
            print(f"❌ Fel vid sparande till Azure: {e}")

    def show_history(self):
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT TOP 5 Timestamp, City, Temperature, Description FROM WeatherData ORDER BY Timestamp DESC")
            rows = cursor.fetchall()

            if not rows:
                print("No history found.")
            else:
                print("\n--- WEATHER SEARCH HISTORY ---")
                print(
                    f"{'DATE & TIME':<20} | {'CITY':<15} | {'TEMP':<7} | {'CONDITION'}")
                print("-" * 65)

                for time, city, temp, desc in rows:
                    clean_time = time.strftime('%Y-%m-%d %H:%M')
                    print(f"{clean_time:<18} | {city:<12} | {temp:>5}°C | {desc}")
            conn.close()
        except Exception as e:
            print(f" Erorr reading from database {e}")

    def delete_history(self):
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM WeatherData")

            conn.commit()
            conn.close()
            print("\n--- History has been cleard succesfully ---")
        except Exception as e:
            print(f"Error deleting history: {e}")

    def set_defult_city(self, city):
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            # 1. Ta bort om den redan finns
            cursor.execute("DELETE FROM setting WHERE name = 'default_city'")

            # 2. Lägg till den nya staden
            cursor.execute(
                "INSERT INTO setting (name, value) VALUES (?,?)",
                ("default_city", city)
            )

            conn.commit()
            conn.close()
            print(f"✅ Default city set to {city} in Azure")
        except Exception as e:
            print(f"❌ Fel vid inställning: {e}")

    def get_defult_city(self):
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()  # Se till att det står conn.cursor() här!
            cursor.execute(
                "SELECT value FROM setting WHERE name = 'default_city'")
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else None
        except Exception as e:
            print(f"Error fetching default city: {e}")
            return None
