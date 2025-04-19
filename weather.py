import requests
from dotenv import load_dotenv
import os

load_dotenv()

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
        print(f"\nCurrent weather in {city.title()}:")
        print(f"{weather.capitalize()}, {temp}°F")
    else:
        print("Error getting weather. Check the city name.")

if __name__ == "__main__":
    city = input("Enter your city: ")
    get_weather(city)