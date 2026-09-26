import os
import requests
from langchain.tools import tool

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert amount from one currency to another using real-time exchange rates."""
    key = os.getenv("EXCHANGE_RATE_API_KEY")
    res = requests.get(f"https://v6.exchangerate-api.com/v6/{key}/latest/{from_currency}").json()
    rate = res.get("conversion_rates", {}).get(to_currency, 1.0)
    return f"{amount * rate:.2f} {to_currency}"

class CurrencyConverterTool:
    currency_converter_tool_list = [convert_currency]