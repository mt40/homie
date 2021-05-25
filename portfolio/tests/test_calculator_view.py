from django.urls import reverse

from admin_site.const import UrlName
from common.tests import BaseTestCase


class CalculatorViewTests(BaseTestCase):
    def test_result_view_context(self):
        url = reverse(
            UrlName.CALCULATOR_RESULT.value,
            kwargs={'result': 999}
        )

        res = self.client.get(url)
        self.assertContains(res, text='999', count=1)

    def test_calculator_view_get(self):
        url = reverse(UrlName.CALCULATOR.value)

        res = self.client.get(url)
        self.assertContains(res, text='Possible loss over', count=1)

    def test_calculator_form_valid_redirect(self):
        res = self.client.post(
            reverse(UrlName.CALCULATOR.value),
            data={
                'risk': 1,
                'buy_price': 2,
                'stop_loss': 3,
                'trading_fee': 4,
            }
        )
        self.assertRedirects(
            res,
            expected_url=reverse(UrlName.CALCULATOR_RESULT.value, kwargs={
                'result': 10
            })
        )