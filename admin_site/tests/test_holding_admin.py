from django.urls import reverse

from admin_site.const import UrlName
from common.tests import BaseTestCase
from portfolio.models import Holding


class HoldingAdminTests(BaseTestCase):
    def test_hiding_empty_holding(self):
        Holding.objects.create(symbol='aaa')
        Holding.objects.create(symbol='bbb', amount=10)

        res = self.client.get(reverse(UrlName.HOLDING_CHANGE_LIST))
        self.assertNotContains(res, 'aaa')
        self.assertContains(res, 'bbb')