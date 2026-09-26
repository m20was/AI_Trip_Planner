import os
import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current temperature and weather conditions for a city."""
    key = os.getenv("OPENWEATHERMAP_API_KEY")
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric").json()
    if "main" in res:
        return f"{city}: {res['main']['temp']}°C, {res['weather'][0]['description']}"
    return f"Could not fetch weather for {city}"

class WeatherInfoTool:
    weather_tool_list = [get_weather]