from langchain.tools import tool

@tool
def calculate_expenses(costs: list[float]) -> float:
    """Calculate the total expense by summing a list of item costs."""
    return round(sum(costs), 2)

class CalculatorTool:
    calculator_tool_list = [calculate_expenses]