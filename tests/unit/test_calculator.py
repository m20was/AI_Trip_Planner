import pytest
from utils.expense_calculator import Calculator

# @pytest.mark.parametrize runs the same test function multiple times
# with different sets of inputs (total, days, expected).
@pytest.mark.parametrize("total, days, expected", [
    (100.0, 5, 20.0),   # Case 1: Normal calculation
    (100.0, 0, 0.0),    # Case 2: Division by zero edge case
    (0.0, 10, 0.0),     # Case 3: Zero total
])
def test_daily_budget(total, days, expected):
    result = Calculator.calculate_daily_budget(total, days)
    assert result == expected
