import datetime
from typing import List, Tuple

import pydantic
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView
from pydantic import PositiveInt, NonNegativeInt

from common import datetime_util
from common.datetime_util import DATE_FORMAT
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
def get_expense_context(
    from_date: datetime.date,
    to_date: datetime.date,
    past_months_expense: int = 2
) -> dict:
    """
    Args:
        from_date: compute expense from this day of the month
        to_date: compute expense to (inclusive) this day of the month
        past_months_expense: number of previous months to compute expense
    """

    this_year = from_date.year
    this_month = from_date.month

    expenses_by_time_range = _get_expense_info_in(
        [
            (
                from_date, to_date
            ),
            *[
                (
                    datetime_util.same_date_in(this_year, this_month - month, from_date),
                    datetime_util.same_date_in(this_year, this_month - month, to_date)
                )
                for month in range(0, past_months_expense)
            ],
        ],
    )
    past_expenses = expenses_by_time_range[1:]

    return {
        'current_total': expenses_by_time_range[0].value,
        'current_avg': expenses_by_time_range[0].daily_avg,
        'past_expense_info': [
            ex.dict() for ex in past_expenses
        ],
        'budgets': Budget.objects.all()
    }


class ExpenseReportForm(forms.Form):
    from_date = forms.DateField(
        initial=datetime_util.first_date_current_month(),
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
    )
    to_date = forms.DateField(
        initial=datetime_util.today(),
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
    )

    def clean(self):
        super().clean()

        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if from_date > to_date:
            raise ValidationError("from_date must not be later than to_date")


class ExpenseReportView(TemplateView):
    template_name = "money/expense_report/index.html"

    def get_context_data(self, **kwargs):
        form = ExpenseReportForm({
            'from_date': kwargs['from_date'],
            'to_date': kwargs['to_date'],
        })

        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']

            if from_date.month == to_date.month:
                extra_context = get_expense_context(from_date, to_date)
            else:
                extra_context = get_expense_context(
                    from_date,
                    to_date,
                    past_months_expense=0,
                )
        else:
            extra_context = {}

        return {
            **super().get_context_data(**kwargs),
            'form': form,
            **extra_context,
        }


class ExpenseReportDefaultView(RedirectView):
    permanent = True
    url = reverse_lazy("homie_admin:expense_report", kwargs={
        'from_date': datetime_util.first_date_current_month().strftime(DATE_FORMAT),
        'to_date': datetime_util.today().strftime(DATE_FORMAT),
    })
