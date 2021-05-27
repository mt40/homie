from django.test import TestCase
from django.urls import reverse

from admin_site.const import UrlName
from portfolio.views import CalculatorComputeResult


class AdminUrlsTests(TestCase):
    def test_reverse_calculator(self):
        reverse(UrlName.CALCULATOR.value)

    def test_reverse_calculator_result(self):
        reverse(UrlName.CALCULATOR_RESULT.value, kwargs=CalculatorComputeResult(
            fund=1,
            risking_cash=2,
            stop_loss_percent=3,
            suggested_buy_amount=4,
            total_buy_value=5,
            suggested_sell_prices='10 - 20',
        ).dict())
