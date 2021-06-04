from common.tests import BaseTestCase
from django.urls import reverse

from admin_site.const import UrlName


class AdminIndexTests(BaseTestCase):
    def test_calculator_link(self):
        url = reverse(UrlName.APP_INDEX.value, args=("portfolio",))
        res = self.client.get(url)
        self.assertContains(
            res,
            text='Calculator'
        )
        self.assertContains(
            res,
            text=reverse(UrlName.CALCULATOR.value)
        )