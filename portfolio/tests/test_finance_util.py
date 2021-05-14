from django.test import TestCase

from portfolio import finance_util
from portfolio.models import Holding


class FinanceUtilTests(TestCase):
    def test_get_net_worth_zero(self):
        self.assertEqual(0, finance_util.get_net_worth())

    def test_get_net_worth(self):
        Holding(
            symbol="A",
            amount=10,
            latest_price=2,
        ).save()
        Holding(
            symbol="B",
            amount=1,
            latest_price=5,
        ).save()

        expect = 10 * 2 + 1 * 5
        rs = finance_util.get_net_worth()

        self.assertEqual(expect, rs)
