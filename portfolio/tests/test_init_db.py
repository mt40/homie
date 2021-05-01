from django.core.management import call_command
from django.test import TestCase

from portfolio.const import TransactionType
from portfolio.management.commands import init_db
from portfolio.models import Transaction


class InitDBTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command(init_db.Command())

    def test_sell_txn(self):
        transactions = Transaction.objects.order_by('transaction_time').all()
        holdings = {}

        for txn in transactions:
            if txn.type == TransactionType.SELL:
                holdings[txn.symbol] = holdings.get(txn.symbol, 0) - txn.amount
            else:
                holdings[txn.symbol] = holdings.get(txn.symbol, 0) + txn.amount

            self.assertGreaterEqual(holdings[txn.symbol], 0, msg=txn.symbol)
