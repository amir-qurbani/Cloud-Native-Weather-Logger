import requests
import os
import pyodbc
from datetime import datetime
import logging
import sqlite3  # For local backup


class WeatherManager:

    # Step 1: Initialize with API key and database connection string
    def __init__(self, api_key, conn_str):
        self.api_key = api_key
        self.conn_str = conn_str

    def get_weather(self, city):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                print(f"Error: Could not find city '{city}'")
                return None
            return data
        except Exception as e:
            print(f"Oops, something went wrong: {e}")
            return None

    def save_to_azure(self, data):
        try:
            city = data["name"]
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO WeatherData (city, temperature, description) VALUES (?,?,?)",
                (city, temp, desc)
            )

            conn.commit()
            conn.close()
            print(f"Saved to Azure: {city}")
        except Exception as e:
            print(f"Error saving to Azure: {e}")
            self.save_locally(data)

    def save_locally(self, data):
        try:
            conn = sqlite3.connect('local_weather.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS WeatherData (
                    City TEXT, 
                    Temperature REAL, 
                    Description TEXT, 
                    Timestamp TEXT
                )
            ''')

            city = data.get("name")
            temp = data.get("main", {}).get("temp")
            desc = data.get("weather", [{}])[0].get("description")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "INSERT INTO WeatherData (City, Temperature, Description, Timestamp) VALUES (?, ?, ?, ?)",
                (city, temp, desc, timestamp)
            )

            conn.commit()
            conn.close()
            print("Data saved locally in local_weather.db!")
        except Exception as le:
            print(f"Could not save locally: {le}")

    def display_weather(self, data):
        if data:
            city_name = data["name"]
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            print(f"In {city_name} it is {temp} degrees and {description}.")

    def show_history(self):
        # 1. Try Azure first
        try:
            conn = pyodbc.connect(self.conn_str, timeout=3)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT TOP 10 Timestamp, City, Temperature, Description FROM WeatherData ORDER BY Timestamp DESC")
            rows = cursor.fetchall()
            print("\n--- CLOUD HISTORY (AZURE) ---")
            self._print_history_rows(rows)
            conn.close()
            return
        except Exception:
            print("\nAzure not available. Loading local history...")

        # 2. Backup: Fetch from SQLite
        try:
            conn = sqlite3.connect('local_weather.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Timestamp, City, Temperature, Description FROM WeatherData ORDER BY Timestamp DESC LIMIT 10")
            rows = cursor.fetchall()
            print("\n--- LOCAL BACKUP HISTORY (SQLite) ---")
            self._print_history_rows(rows)
            conn.close()
        except Exception as e:
            print(f"Could not fetch history: {e}")

    def _print_history_rows(self, rows):
        if not rows:
            print("No history found.")
            return
        print(f"{'TIME':<20} | {'CITY':<15} | {'TEMP':<7} | {'WEATHER'}")
        print("-" * 65)
        for row in rows:
            time_val = str(row[0])[:16]
            print(f"{time_val:<20} | {row[1]:<15} | {row[2]:>5}°C | {row[3]}")
