from typing import List, Iterable

import numpy as np
from numpy import sin
from scipy.optimize import curve_fit


def expense_projection(current_expenses: List[int], project_for: Iterable[int]) -> List[int]:
    """
    Returns a projection (i.e. predictions) of future expenses based on current expenses.

    Implementation:
        We consider this as a regression problem so we just need to find a suitable function
        to fit our data. Since expense is not a smooth line, it usually has ups and downs.
        We choose a sin function to integrate that.

        Also, we may have very little training data (e.g. at the beginning of the month),
        we choose an optimization method called 'dogbox', which can handle little data.
        See the links below for more details.

    Args:
        current_expenses: current expenses, used as training data
        project_for: the input x values to predict

    See Also:
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html#scipy.optimize.least_squares

    """

    def objective(x, a, b, c):
        return a * sin(x) + b * x ** 1.2 + c

    x_values = np.array(range(1, len(current_expenses) + 1))
    y_values = np.array(current_expenses)

    coefficients, _ = curve_fit(objective, x_values, y_values, method='dogbox')

    x_new = np.array(project_for)

    # use optimal coefficients to calculate new values
    return [int(y) for y in objective(x_new, *coefficients)]