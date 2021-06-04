from django.urls import reverse

from admin_site.const import UrlName
from common.tests import BaseTestCase
from portfolio.views import CalculatorComputeResult, CalculatorView


class CalculatorViewTests(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_result = CalculatorComputeResult(
            fund=111,
            risking_cash=222,
            stop_loss_percent=20.5,
            suggested_buy_amount=333,
            total_buy_value=444,
            suggested_sell_prices='10 - 20',
        )

    def test_result_view_context(self):
        url = reverse(
            UrlName.CALCULATOR_RESULT.value,
            kwargs=self.test_result.dict()
        )

        res = self.client.get(url)
        for k, v in self.test_result.dict().items():
            self.assertContains(res, text=k)
            self.assertContains(res, text=v)

    def test_calculator_view_get(self):
        url = reverse(UrlName.CALCULATOR.value)

        res = self.client.get(url)
        self.assertContains(res, text='Possible loss over', count=1)

    def test_calculator_form_valid_redirect(self):
        data = {
            'risk': 1,
            'buy_price': 2,
            'stop_loss': 3,
            'trading_fee': 4,
        }
        result = CalculatorView.compute(**data)

        res = self.client.post(
            reverse(UrlName.CALCULATOR.value),
            data=data
        )
        self.assertRedirects(
            res,
            expected_url=reverse(
                UrlName.CALCULATOR_RESULT.value,
                kwargs=result.dict()
            )
        )
