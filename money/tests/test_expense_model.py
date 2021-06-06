from common import datetime_util
from common.tests import BaseTestCase, WithFakeData
from money.models import Expense, Wallet, ExpenseCategory


class ExpenseModelTests(WithFakeData, BaseTestCase):
    def test_get_expenses_in(self):
        Expense.objects.all().delete()
        self.assertEqual(
            0,
            Expense.get_expenses_in(
                start_date=datetime_util.today(),
                end_date=datetime_util.today(),
            ).count()
        )

        e = Expense.objects.create(
            wallet=Wallet.objects.first(),
            category=ExpenseCategory.objects.first(),
            value=199,
        )
        self.assertEqual(
            e,
            Expense.get_expenses_in(
                start_date=datetime_util.today(),
                end_date=datetime_util.today(),
            ).get()
        )
