import datetime
from typing import List, Tuple

import pydantic
from django.views.generic import TemplateView
from pydantic import PositiveInt, NonNegativeInt

from common import datetime_util
from money.models import Budget, Expense


class PreviousExpenseInfo(pydantic.BaseModel):
    name: str
    value: NonNegativeInt
    # change compared to the first time range
    value_change_percent: int

    daily_avg: NonNegativeInt
    daily_avg_change_percent: int


def _get_expense_info_in(
    time_ranges: List[Tuple[datetime.date, datetime.date]],
) -> List[PreviousExpenseInfo]:
    """
    Get expense info in each time range.
    """
    first_value = 0
    first_avg = 0

    rs = []
    for i, (from_date, to_date) in enumerate(time_ranges):
        value = Expense.get_expense_value_in(from_date, to_date)
        value_change_percent = (
            int((first_value - value) / value * 100)
            if value != 0 and i > 0
            else 0
        )

        average = (
            value / (to_date - from_date).days
            if to_date != from_date
            else value
        )
        avg_change_percent = (
            int((first_avg - average) / average * 100)
            if average != 0 and i > 0
            else 0
        )

        info = PreviousExpenseInfo(
            name=from_date.strftime("%b"),
            value=value,
            value_change_percent=value_change_percent,
            daily_avg=average,
            daily_avg_change_percent=avg_change_percent,
        )

        rs.append(info)

        if i == 0:
            first_value = value
            first_avg = average

    return rs


# testme
class ExpenseReportView(TemplateView):
    template_name = "money/expense_report/index.html"

    def get_context_data(self, **kwargs):
        today = datetime_util.today()
        this_year = today.year
        this_month = today.month

        expenses_by_time_range = _get_expense_info_in(
            [
                (
                    datetime_util.first_date_of(this_year, this_month),
                    datetime_util.today(),
                ),
                (
                    datetime_util.first_date_of(this_year, this_month - 1),
                    datetime_util.same_date_in(this_year, this_month - 1, today)
                ),
                (
                    datetime_util.first_date_of(this_year, this_month - 2),
                    datetime_util.same_date_in(this_year, this_month - 2, today)
                ),
            ],
        )
        past_expenses = expenses_by_time_range[1:]

        return {
            **super().get_context_data(**kwargs),
            'current_total': expenses_by_time_range[0].value,
            'current_avg': expenses_by_time_range[0].daily_avg,
            'past_expense_info': [
                ex.dict() for ex in past_expenses
            ],
            'budgets': Budget.objects.all()
        }
