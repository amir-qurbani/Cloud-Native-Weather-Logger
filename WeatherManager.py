import requests
import os
from dotenv import load_dotenv


class WeatherManager:

    def __init__(self, api_key):
        self.api_key = api_key

    def hämta_väder(self, stad):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={stad}&appid={self.api_key}&units=metric"

            svar = requests.get(url)
            data = svar.json()
            return data
        except Exception as e:
            print(f"Hoppsan, något gick fel: {e}")

    def presentera_väder(self, data):
        stad = data["name"]
        temp = data["main"]["temp"]
        beskrivning = data["weather"][0]["description"]

        print(f"I {stad} är det {temp} grader och {beskrivning}")


load_dotenv()
hemlig_nycket = os.getenv("API_KEY")

min_väder_app = WeatherManager(hemlig_nycket)
resultat = min_väder_app.hämta_väder("Paris")
min_väder_app.presentera_väder(resultat)
print(resultat)
