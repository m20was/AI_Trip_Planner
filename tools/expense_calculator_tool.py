from langchain.tools import tool
from utils.expense_calculator import Calculator

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        
        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool
        def calculate_total_expense(costs: list[float]) -> float:
            """Calculate total expense of the trip from a list of costs"""
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        self.calculator_tool_list = [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget
        ]