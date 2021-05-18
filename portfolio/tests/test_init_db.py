from django.core.management import call_command
from django.test import TestCase

from admin_site.management.commands import init_db
from portfolio.models import Transaction, Holding


class InitDBTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command(init_db.Command())

    def test_sell_txn(self):
        holdings = Holding.objects.all()
        for holding in holdings:
            self.assertGreaterEqual(holding.amount, 0)
