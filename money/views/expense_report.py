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
    change_percent: int


def _get_previous_expenses(
    time_ranges: List[Tuple[datetime.date, datetime.date]],
    current_expense: int
) -> List[PreviousExpenseInfo]:
    rs = []
    for from_date, to_date in time_ranges:
        value = Expense.get_expense_value_in(from_date, to_date)
        change_percent = int(100 - value / current_expense) if current_expense != 0 else 0
        info = PreviousExpenseInfo(
            name=from_date.strftime("%b"),
            value=Expense.get_expense_value_in(from_date, to_date),
            change_percent=change_percent
        )
        rs.append(info)
    return rs


class ExpenseReportView(TemplateView):
    template_name = "money/expense_report/index.html"

    def get_context_data(self, **kwargs):
        from_date = datetime_util.first_date_current_month()
        to_date = datetime_util.today()

        total_expense_value = Expense.get_expense_value_in(
            from_date,
            to_date,
        )

        this_year = from_date.year
        this_month = from_date.month
        previous_expenses = _get_previous_expenses(
            [
                (
                    datetime_util.first_date_of(this_year, this_month - 1),
                    datetime_util.same_date_in(this_year, this_month - 1, to_date)
                ),
                (
                    datetime_util.first_date_of(this_year, this_month - 2),
                    datetime_util.same_date_in(this_year, this_month - 2, to_date)
                ),
            ],
            total_expense_value
        )

        days = (to_date - from_date).days
        avg_expense_value = int(total_expense_value / days)

        return {
            **super().get_context_data(**kwargs),
            'total_expense': {
                'current': total_expense_value,
                'previous': [
                    ex.dict()
                    for ex in previous_expenses
                ]
            },
            'avg_expense_value': avg_expense_value,
            'budgets': Budget.objects.all()
        }
