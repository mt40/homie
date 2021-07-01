from datetime import timedelta, date

from unittest.mock import patch

from admin_site import admin
from common import datetime_util
from common.tests import BaseTestCase, WithFakeData
from money.models import Expense, ExpenseGroup, Wallet, ExpenseCategory


class BudgetAdminTests(WithFakeData, BaseTestCase):
    def test_get_y_values(self):
        expenses, index = admin._get_y_values(ExpenseGroup.objects.first())
        self.assertEqual(datetime_util.last_date_current_month().day, len(expenses))
        self.assertEqual(datetime_util.today().day - 1, index)

    @patch.object(datetime_util, 'today', lambda: date(2021, 7, 1))
    def test_get_current_accumulated_expenses_first_day(self):
        group = ExpenseGroup.objects.first()
        day1 = datetime_util.first_date_current_month()
        day1_expense = Expense.get_expense_value_in(day1, day1, group=group)

        rs = admin._get_current_accumulated_expenses(group)
        self.assertCountEqual([day1_expense], rs)

    @patch.object(datetime_util, 'today', lambda: date(2021, 7, 3))
    def test_get_current_accumulated_expenses(self):
        group = ExpenseGroup.objects.first()
        day1 = datetime_util.first_date_current_month()
        day1_expense = Expense.get_expense_value_in(day1, day1, group=group)

        day2 = day1 + timedelta(days=1)
        Expense.objects.create(
            wallet=Wallet.objects.first(),
            category=ExpenseCategory.objects.filter(group=group).first(),
            value=50,
            pay_date=day2,
        )
        day2_expense = Expense.get_expense_value_in(day2, day2, group=group)

        rs = admin._get_current_accumulated_expenses(group)
        self.assertEqual(day1_expense, rs[0])
        self.assertEqual(day1_expense + day2_expense, rs[1])
