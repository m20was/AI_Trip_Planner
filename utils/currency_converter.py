import requests

class CurrencyConverter:
    def __init__(self, api_key: str):
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert the amount from one currency to another"""
        response = requests.get(f"{self.base_url}{from_currency}")
        if response.status_code != 200:
            raise Exception("API call failed:", response.json())
        rates = response.json().get("conversion_rates", {})
        if to_currency not in rates:
            raise ValueError(f"{to_currency} not found in exchange rates.")
        return amount * rates[to_currency]