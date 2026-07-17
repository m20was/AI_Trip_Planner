import os
from langchain.tools import tool
from utils.weather_info import WeatherForecastTool

class WeatherInfoTool:
    def __init__(self):
        api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.weather_service = WeatherForecastTool(api_key)
        
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            data = self.weather_service.get_current_weather(city)
            if data:
                temp = data.get('main', {}).get('temp', 0)
                temp = round(temp - 273.15, 1) if temp > 150 else temp
                desc = data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Could not fetch weather for {city}"
        
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            data = self.weather_service.get_forecast_weather(city)
            if data and 'list' in data:
                forecasts = []
                for item in data['list']:
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    temp = round(temp - 273.15, 1) if temp > 150 else temp
                    desc = item['weather'][0]['description']
                    forecasts.append(f"{date}: {temp}°C, {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecasts)
            return f"Could not fetch forecast for {city}"
            
        self.weather_tool_list = [get_current_weather, get_weather_forecast]