from datetime import timedelta

from django.core.exceptions import ValidationError
from django.urls import reverse

from common import datetime_util
from common.tests import BaseTestCase
from money.views.expense_report import ExpenseReportForm

_default_expense_report_url = reverse("homie_admin:expense_report_default")


class ExpenseReportViewTests(BaseTestCase):
    def test_expense_report_view_get(self):
        self.client.get(_default_expense_report_url)

    def test_expense_report_view_context(self):
        expense_this_month = ...
        expense_change_percent = ...
        avg_daily_expense = ...
        avg_daily_change_percent = ...
        today_expense = ...
        budget_names = ...

        res = self.client.get(_default_expense_report_url)

        self.assertContains(res, expense_this_month)
        self.assertContains(res, expense_change_percent)
        self.assertContains(res, avg_daily_expense)
        self.assertContains(res, avg_daily_change_percent)
        self.assertContains(res, today_expense)
        for name in budget_names:
            self.assertContains(res, name)

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
