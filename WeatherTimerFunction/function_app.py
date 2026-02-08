import azure.functions as func
import logging
import os
from WeatherManager import WeatherManager

app = func.FunctionApp()


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:

    api_key = os.getenv("OPENWEATHER_API_KEY")
    conn_str = os.getenv("AZURE_CONNECTION_STRING")

    if myTimer.past_due:
        logging.info('The timer is past due!')

    weather_app = WeatherManager(api_key, conn_str)

    weather_data = weather_app.get_weather("Stockholm")

    if weather_data:
        weather_app.save_to_azure(weather_data)
        logging.info("The weather was saved automatically!")
