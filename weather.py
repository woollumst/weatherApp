import requests
from dotenv import load_dotenv
import os
from colorama import init, Fore, Style

init(autoreset=True) # Colorama Settings
load_dotenv() # Load API_KEY from .env

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        print(Fore.GREEN + f"\nCurrent weather in {city.title()}:" + Style.RESET_ALL)
        print(f"{weather.capitalize()}, {temp}°F")
    else:
        print("Error getting weather. Check the city name.")

def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"
    }
    response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
    if response.status_code == 200:
        data = response.json()
        print(Fore.GREEN + f"\n5-Day Forecast for {city.title()}:")

        forecast_by_day = {}

        for entry in data["list"]:
            date, time = entry["dt_txt"].split()
            if time in ["06:00:00", "12:00:00", "18:00:00"]: # Show just midday
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]

                rain_mm = entry.get("rain", {}).get("3h", 0)
                rain_in = round(rain_mm * 0.03937, 2)
                rain_info = f" | Rain: {rain_in} in" if rain_in > 0 else ""

                time_label = {"06:00:00": "Morning", "12:00:00": "Midday", "18:00:00": "Night"}[time]
                forecast = f"{time_label}: {desc.capitalize()}, {temp}°F{rain_info}"
                
                if date not in forecast_by_day:
                    forecast_by_day[date] = []
                forecast_by_day[date].append(forecast)

        for date in sorted(forecast_by_day.keys()):
            print(Fore.GREEN + Style.DIM + f"{date}:")
            for forecast in forecast_by_day[date]:
                print(f"    {forecast}")
            print()

    else:
        print("Error getting forecast. Check the city name.")

if __name__ == "__main__":
    city = input(Fore.YELLOW + "Enter your city: ")
    get_weather(city)
    get_forecast(city)