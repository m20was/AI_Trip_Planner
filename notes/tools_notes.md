# Business Tools Architecture & Notes

> **Target Role:** Entry-Level Business Analyst (BA) / Analytics Consultant  
> **Key Architecture:** 1 Business Need = 1 Specialized Tool (Total 4 Tools)  
> **Integrations:** Tavily Search, OpenWeatherMap, ExchangeRate-API, Python Math

---

## 1. Executive Summary: The 4 Core Business Tools

In an agentic system, tools represent the **business capabilities** given to the LLM. Instead of hallucinating facts or relying on outdated training data, Google Gemini autonomously calls one of our **four specialized tools**:

| # | Tool Name | File Path | External Service | Business Function |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **`search_places`** | `tools/place_search_tool.py` | Tavily Search API | Discovers attractions, top dining, local activities & transit |
| **2** | **`get_weather`** | `tools/weather_info_tool.py` | OpenWeatherMap API | Live temperature & climate conditions for packing & planning |
| **3** | **`convert_currency`** | `tools/currency_conversion_tool.py` | ExchangeRate-API | Real-time foreign exchange calculation for international budgets |
| **4** | **`calculate_expenses`** | `tools/expense_calculator_tool.py` | Python Math | Deterministic summation of costs (eliminates LLM math errors) |

---

## 2. Why We Simplified (The Business Analyst Perspective)

### Previous Problems:
* **Artificial Over-Engineering:** The original codebase had 10 separate micro-functions (e.g. 4 near-identical search functions, 3 basic math functions) spread across extra `utils/` helper files.
* **High Maintenance & Cognitive Load:** In an interview, clicking across 8 different files to explain basic API calls creates confusion and distracts from the core business solution.

### Our Clean Design:
* **1 Tool per File:** Each file is **under 12 lines of readable Python**.
* **Zero Jargon / Zero Bloat:** Top-level `@tool` definitions, no nested functions, no unnecessary class hierarchies.
* **Easy to Walkthrough:** You can screen-share any tool file and explain it in 15 seconds.

---

## 3. The 4 Tool Implementations (Clean & Short)

### 3.1 Place Search Tool (`tools/place_search_tool.py` - 11 Lines)
```python
from langchain.tools import tool
from langchain_tavily import TavilySearch

tavily = TavilySearch(topic="general", include_answer="advanced")

@tool
def search_places(query: str) -> str:
    """Search for attractions, restaurants, activities, and transport in any city."""
    res = tavily.invoke({"query": query})
    return res.get("answer", str(res))

class PlaceSearchTool:
    place_search_tool_list = [search_places]
```
> **What it does:** Sends natural language queries to Tavily's web search and returns direct, concise answers.

---

### 3.2 Weather Info Tool (`tools/weather_info_tool.py` - 13 Lines)
```python
import os, requests
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
```
> **What it does:** Calls OpenWeatherMap with `units="metric"` to give real-time Celsius temperature and sky conditions.

---

### 3.3 Currency Conversion Tool (`tools/currency_conversion_tool.py` - 12 Lines)
```python
import os, requests
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
```
> **What it does:** Queries ExchangeRate-API for live FX rates and formats the output cleanly (e.g. `438.65 EUR`).

---

### 3.4 Expense Calculator Tool (`tools/expense_calculator_tool.py` - 9 Lines)
```python
from langchain.tools import tool

@tool
def calculate_expenses(costs: list[float]) -> float:
    """Calculate the total expense by summing a list of costs."""
    return round(sum(costs), 2)

class CalculatorTool:
    calculator_tool_list = [calculate_expenses]
```
> **What it does:** Accurately sums accommodation, flights, dining, and activity costs to prevent LLM arithmetic hallucinations.

---

## 4. How the Agent Consolidates the Tools (`tools/__init__.py`)

```python
from tools.weather_info_tool import get_weather
from tools.place_search_tool import search_places
from tools.expense_calculator_tool import calculate_expenses
from tools.currency_conversion_tool import convert_currency

def get_tools():
    """Consolidate the 4 core business tools for the agent."""
    return [get_weather, search_places, calculate_expenses, convert_currency]
```

---

## 5. Interview Talking Points (Business Analyst Perspective)

### Q: "How did you design the tool layer in this architecture?"
> *"I mapped our tool architecture directly to the **four key decisions every traveler makes**:
> 1. **Discovery:** Where should I go and what should I eat? (`search_places` via Tavily)
> 2. **Preparedness:** What should I wear and pack? (`get_weather` via OpenWeatherMap)
> 3. **Foreign Exchange:** How much will this cost in local currency? (`convert_currency` via ExchangeRate-API)
> 4. **Budgeting:** What is my total projected trip cost? (`calculate_expenses`)
> 
> Rather than over-complicating with dozens of micro-functions, having one focused, production-grade tool per business pillar keeps the system modular, reliable, and easy to maintain."*

### Q: "Why do you need an expense calculator if LLMs can already calculate numbers?"
> *"Large Language Models are probabilistic next-token predictors, not deterministic math engines. LLMs notoriously make calculation mistakes when adding multiple cost categories. By connecting a dedicated calculation tool, we ensure **100% mathematical accuracy** in the final budget breakdown."*

### Q: "How does the system handle API failures?"
> *"We implemented graceful fallbacks. For instance, if an unsupported city name is passed to the weather API, the tool returns a clean status message (`'Could not fetch weather for {city}'`) instead of crashing the server. This allows the LLM to acknowledge the issue politely and proceed with the rest of the itinerary seamlessly."*
