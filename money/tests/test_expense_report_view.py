import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.urls import reverse

from common import datetime_util
from common.datetime_util import DATE_FORMAT
from common.tests import BaseTestCase
from money.models import Expense, Budget
from money.views.expense_report import ExpenseReportForm

_default_expense_report_url = reverse("homie_admin:expense_report_default")

def _expense_report_url(start: datetime.date, end: datetime.date):
    return reverse(
        "homie_admin:expense_report",
        args=(start.strftime(DATE_FORMAT), end.strftime(DATE_FORMAT))
    )


class ExpenseReportViewTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.month_start = datetime_util.first_date_current_month()
        self.month_end = datetime_util.today()
        self.this_month_report_url = _expense_report_url(self.month_start, self.month_end)

    def test_expense_report_view_redirect(self):
        res = self.client.get(_default_expense_report_url)
        self.assertEqual(301, res.status_code)
        self.assertEqual(
            _expense_report_url(datetime_util.first_date_current_month(), datetime_util.today()),
            res.url
        )

    def test_expense_report_overview_context(self):
        expense_this_month = Expense.get_expense_value_in(self.month_start, self.month_end)
        days = (self.month_end - self.month_start).days + 1
        avg_expense = int(expense_this_month / days)
        one_month_ago = self.month_start - relativedelta(months=1)
        two_month_ago = self.month_start - relativedelta(months=2)

        res = self.client.get(self.this_month_report_url)

        self.assertContains(res, expense_this_month)
        self.assertContains(res, avg_expense)
        self.assertContains(res, one_month_ago.strftime('%b'))
        self.assertContains(res, two_month_ago.strftime('%b'))

    def test_expense_report_budget_context(self):
        budgets = Budget.objects.all()

        res = self.client.get(self.this_month_report_url)

        for budget in budgets:
            self.assertContains(budget.expense_group.name, res)
            self.assertContains(budget.current_percent, res)

    def test_expense_report_daily_context(self):
        ...  # todo

    def test_expense_report_category_context(self):
        ...  # todo

    def test_expense_report_form_validation_ok(self):
        def check(from_date, to_date):
            data = {'from_date': from_date, 'to_date': to_date}
            self.assertTrue(ExpenseReportForm(data).is_valid())

        check(datetime_util.today(), datetime_util.tmr())
        check(datetime_util.today(), datetime_util.today())
        check('2021-06-15', '2021-06-30')
        check('2021-06-15', '2021-06-15')

    def test_expense_report_form_validation_fail(self):
        def check(from_date, to_date):
            data = {'from_date': from_date, 'to_date': to_date}
            form = ExpenseReportForm(data)
            self.assertFalse(form.is_valid())

        check(datetime_util.today(), datetime_util.today() - timedelta(days=1))
        check('2021-06-15', '2021-06-14')
        check('2021-06', '2021-06-14')
        check('2021-06-31', '2021-07-01')
