from langgraph.prebuilt import create_react_agent
from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader
from tools.weather_info_tool import get_weather
from tools.place_search_tool import search_places
from tools.expense_calculator_tool import calculate_expenses
from tools.currency_conversion_tool import convert_currency

def get_tools():
    """Consolidate the 4 core business tools for the agent."""
    return [get_weather, search_places, calculate_expenses, convert_currency]

class GraphBuilder:
    def __init__(self, model_provider: str = "gemini"):
        self.llm = ModelLoader(model_provider=model_provider).load_llm()
        self.tools = get_tools()

    def __call__(self):
        """Build and return the compiled ReAct agent."""
        return create_react_agent(self.llm, self.tools, prompt=SYSTEM_PROMPT)