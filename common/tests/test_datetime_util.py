import datetime
from unittest.mock import patch, Mock

from common import datetime_util
from common.tests import BaseTestCase


class DatetimeUtilTests(BaseTestCase):
    def test_first_day_current_month(self):
        rs = datetime_util.first_date_current_month()
        self.assertEqual(1, rs.day)

    @patch.object(datetime_util, 'today')
    def test_last_day_current_month(self, today_mock: Mock):
        today_mock.return_value = datetime.date.today().replace(month=1)
        self.assertEqual(31, datetime_util.last_date_current_month().day)

        today_mock.return_value = datetime.date.today().replace(month=4)
        self.assertEqual(30, datetime_util.last_date_current_month().day)

        today_mock.return_value = datetime.date.today().replace(
            year=2021, month=2
        )
        self.assertEqual(28, datetime_util.last_date_current_month().day)

    def test_get_date_iterator(self):
        def _check(start, end, expect):
            rs = list(datetime_util.get_date_iterator(start, end))
            self.assertCountEqual(expect, rs)

        _check(
            start=datetime.date(year=2021, month=5, day=31),
            end=datetime.date(year=2021, month=6, day=2),
            expect=[
                datetime.date(year=2021, month=5, day=31),
                datetime.date(year=2021, month=6, day=1),
                datetime.date(year=2021, month=6, day=2),
            ]
        )
        _check(
            start=datetime.date(year=2021, month=5, day=31),
            end=datetime.date(year=2021, month=5, day=29),
            expect=[]
        )
        _check(
            start=datetime.date(year=2021, month=5, day=31),
            end=datetime.date(year=2021, month=5, day=31),
            expect=[datetime.date(year=2021, month=5, day=31)]
        )
