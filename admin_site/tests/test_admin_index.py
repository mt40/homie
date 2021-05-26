from common.tests import BaseTestCase
from django.urls import reverse

from admin_site.const import UrlName


class AdminIndexTests(BaseTestCase):
    def test_calculator_link(self):
        res = self.client.get(reverse(UrlName.ADMIN_INDEX.value))
        self.assertContains(
            res,
            text='Calculator'
        )
        self.assertContains(
            res,
            text=reverse(UrlName.CALCULATOR.value)
        )