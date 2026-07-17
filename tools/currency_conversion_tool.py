import os
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter

class CurrencyConverterTool:
    def __init__(self):
        api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter(api_key)
        
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
            """Convert amount from one currency to another"""
            return self.currency_service.convert(amount, from_currency, to_currency)
        
        self.currency_converter_tool_list = [convert_currency]