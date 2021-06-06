from common.tests import BaseTestCase, WithFakeData
from money.models import Expense, Wallet, ExpenseCategory, Budget, ExpenseGroup


class BudgetModelTests(WithFakeData, BaseTestCase):
    def test_current_percent(self):
        Expense.objects.all().delete()
        Budget.objects.all().delete()

        wallet = Wallet.objects.first()
        group1, group2 = ExpenseGroup.objects.all()[:2]
        Expense.objects.create(
            wallet=wallet,
            category=ExpenseCategory.objects.filter(group=group1).first(),
            value=200,
        )
        Expense.objects.create(
            wallet=wallet,
            category=ExpenseCategory.objects.filter(group=group2).first(),
            value=10,
        )

        budget1 = Budget.objects.create(expense_group=group1, limit=250)
        budget2 = Budget.objects.create(expense_group=group2, limit=5)

        self.assertEqual(int(200 / 250 * 100), budget1.current_percent)
        self.assertEqual(int(10 / 5 * 100), budget2.current_percent)
