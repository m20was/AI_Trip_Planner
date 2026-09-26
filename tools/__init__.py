from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

def get_tools():
    """Consolidate all business tools for the agent."""
    return [
        *WeatherInfoTool().weather_tool_list,
        *PlaceSearchTool().place_search_tool_list,
        *CalculatorTool().calculator_tool_list,
        *CurrencyConverterTool().currency_converter_tool_list,
    ]
