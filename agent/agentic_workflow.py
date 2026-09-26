from langgraph.prebuilt import create_react_agent
from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader
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

class GraphBuilder:
    def __init__(self, model_provider: str = "gemini"):
        self.llm = ModelLoader(model_provider=model_provider).load_llm()
        self.tools = get_tools()

    def __call__(self):
        """Build and return the compiled ReAct agent."""
        return create_react_agent(self.llm, self.tools, prompt=SYSTEM_PROMPT)