
import pendulum
from django.test import TestCase

from portfolio import time_util


class TimeUtilTests(TestCase):
    def test_from_unix_timestamp(self):
        ts = 1619508998
        expect = pendulum.datetime(year=2021, month=4, day=27, hour=14, minute=36, second=38, tz='Asia/Ho_Chi_Minh')

        self.assertEqual(expect, time_util.from_unix_timestamp(ts))

    def test_from_unix_timestamp_error(self):
        ts = 'a'
        self.assertRaises(TypeError, lambda: time_util.from_unix_timestamp(ts))
