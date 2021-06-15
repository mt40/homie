from datetime import timedelta

from django.core.exceptions import ValidationError
from django.urls import reverse

from common import datetime_util
from common.tests import BaseTestCase
from money.views.expense_report import ExpenseReportForm

_expense_report_url = reverse("homie_admin:expense_report")


class ExpenseReportViewTests(BaseTestCase):
    def test_expense_report_view_get(self):
        self.client.get(_expense_report_url)

    def test_expense_report_view_context(self):
        expense_this_month = ...
        expense_change_percent = ...
        avg_daily_expense = ...
        avg_daily_change_percent = ...
        today_expense = ...
        budget_names = ...

        res = self.client.get(_expense_report_url)

        self.assertContains(res, expense_this_month)
        self.assertContains(res, expense_change_percent)
        self.assertContains(res, avg_daily_expense)
        self.assertContains(res, avg_daily_change_percent)
        self.assertContains(res, today_expense)
        for name in budget_names:
            self.assertContains(res, name)

    def test_expense_report_form_validation_ok(self):
        data = {
            'from_date': datetime_util.today(),
            'to_date': datetime_util.tmr(),
        }
        self.assertTrue(ExpenseReportForm(data).is_valid())

        data = {
            'from_date': datetime_util.today(),
            'to_date': datetime_util.today(),
        }
        self.assertTrue(ExpenseReportForm(data).is_valid())

    def test_expense_report_form_validation_fail(self):
        data = {
            'from_date': datetime_util.today(),
            'to_date': datetime_util.today() - timedelta(days=1),
        }
        form = ExpenseReportForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.non_field_errors()))
        self.assertIn("must not be later", form.non_field_errors()[0])
