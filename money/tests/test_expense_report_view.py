from django.urls import reverse

from common.tests import BaseTestCase


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
