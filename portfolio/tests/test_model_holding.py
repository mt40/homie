from django.test import TestCase

from portfolio.const import TransactionType
from portfolio.models import Holding, Transaction


class ModelHoldingTests(TestCase):
    def test_update_from_transaction(self):
        buy, _ = Transaction.objects.get_or_create(
            symbol='a',
            price=10,
            amount=3,
        )
        holding = Holding.objects.get(symbol=buy.symbol)
        self.assertEqual(10 * 3, holding.total_value)

        sell, _ = Transaction.objects.get_or_create(
            symbol='a',
            type=TransactionType.SELL,
            price=15,
            amount=2,
        )
        holding.refresh_from_db()
        self.assertEqual(15 * 1, holding.total_value)

        sell, _ = Transaction.objects.get_or_create(
            symbol='a',
            type=TransactionType.SELL,
            price=14,
            amount=1,
        )
        holding.refresh_from_db()
        self.assertEqual(0, holding.total_value)