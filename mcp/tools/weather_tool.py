import requests
from mcp.base_tool import MCPTool
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import API_KEY

class WeatherTool(MCPTool):
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current temperature (°C) of a city using OpenWeatherMap"
        )

    def run(self, city):
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # FIX: was data["current"]["temp_c"] — correct key is data["main"]["temp"]
        return data["main"]["temp"]

    def get_full_weather(self, city):
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
        }