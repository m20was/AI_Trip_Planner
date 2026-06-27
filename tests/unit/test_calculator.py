from utils.expense_calculator import Calculator

def test_multiply():
    # Simple unit test: testing one function in isolation
    assert Calculator.multiply(3, 4) == 12

def test_calculate_daily_budget():
    # Unit test: testing function logic with edge case
    assert Calculator.calculate_daily_budget(100.0, 5) == 20.0
    assert Calculator.calculate_daily_budget(100.0, 0) == 0.0
