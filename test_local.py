import os
from dotenv import load_dotenv
from WeatherTimerFunction.WeatherManager import WeatherManager


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def run_local_test():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    conn_str = os.getenv("AZURE_CONNECTION_STRING")

    if not api_key:
        print("Fel: Kunde inte hitta OPENWEATHER_API_KEY i .env filen.")
        return

    mgr = WeatherManager(api_key, conn_str)

    print("Hämtar väder för Stockholm...")
    data = mgr.get_weather("Stockholm")

    if data:

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        city = data["name"]

        print(f"Väder hämtat för {city}: {temp}°C, {desc}")

        mgr.save_to_azure(data)
    else:
        print(f"Data saknar förväntade nycklar: {data}")


if __name__ == "__main__":
    run_local_test()
