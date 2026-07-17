import requests

class WeatherForecastTool:
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place: str) -> dict:
        """Get current weather of a place"""
        url = f"{self.base_url}/weather"
        params = {"q": place, "appid": self.api_key}
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else {}
    
    def get_forecast_weather(self, place: str) -> dict:
        """Get weather forecast of a place"""
        url = f"{self.base_url}/forecast"
        params = {"q": place, "appid": self.api_key, "cnt": 10, "units": "metric"}
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else {}