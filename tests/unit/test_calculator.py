import pytest
from tools.expense_calculator_tool import calculate_expenses

# @pytest.mark.parametrize runs the same test function multiple times
# with different sets of inputs (costs list, expected sum).
@pytest.mark.parametrize("costs, expected", [
    ([100.0, 50.0, 25.5], 175.5),  # Case 1: Normal calculation
    ([], 0.0),                     # Case 2: Empty list
    ([10.25], 10.25),              # Case 3: Single expense
])
def test_calculate_expenses(costs, expected):
    result = calculate_expenses.invoke({"costs": costs})
    assert result == expected
