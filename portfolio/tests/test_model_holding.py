from django.test import TestCase

from portfolio import const
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

    def test_get_fund(self):
        Transaction.objects.get_or_create(
            symbol=const.DEPOSIT_SYMBOL,
            price=10,
            amount=3,
        )
        Transaction.objects.get_or_create(
            symbol=const.DEPOSIT_SYMBOL,
            price=5,
            amount=1,
        )

        expect = 10 * 3 + 5 * 1
        rs = Holding.get_fund()

        self.assertEqual(expect, rs)

    def test_recalculate(self):
        Transaction.objects.create(
            symbol=const.DEPOSIT_SYMBOL,
            price=20,
            amount=1,
        )
        Transaction.objects.create(
            symbol='aaa',
            price=10,
            amount=3,
        )
        Transaction.objects.create(
            symbol='aaa',
            price=5,
            amount=1,
        )

        expect = 5 * 3 + 5 * 1  # latest price is 5
        rs = Holding.objects.get(symbol='aaa').total_value

        self.assertEqual(expect, rs)

    def test_holding_fund(self):
        Transaction.objects.create(
            symbol=const.DEPOSIT_SYMBOL,
            price=100,
            amount=1,
        )
        holding = Holding.objects.get(symbol=const.DEPOSIT_SYMBOL)
        self.assertEqual(100, holding.total_value)

        Transaction.objects.create(
            symbol='aaa',
            price=10,
            amount=1,
        )
        holding.refresh_from_db()
        self.assertEqual(90, holding.total_value)

        Transaction.objects.create(
            symbol='aaa',
            price=1,
            amount=1,
            type=TransactionType.SELL,
        )
        holding.refresh_from_db()
        self.assertEqual(91, holding.total_value)