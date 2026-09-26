from tools.weather_info_tool import get_weather
from tools.place_search_tool import search_places
from tools.expense_calculator_tool import calculate_expenses
from tools.currency_conversion_tool import convert_currency

def get_tools():
    """Consolidate the 4 core business tools for the agent."""
    return [get_weather, search_places, calculate_expenses, convert_currency]
