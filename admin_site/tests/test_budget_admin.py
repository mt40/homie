from admin_site import admin
from common import datetime_util
from common.tests import BaseTestCase, WithFakeData


class BudgetAdminTests(WithFakeData, BaseTestCase):
    def test_get_y_values(self):
        expenses, index = admin._get_y_values()
        self.assertEqual(datetime_util.last_date_current_month().day, len(expenses))
        self.assertEqual(datetime_util.today().day - 1, index)
