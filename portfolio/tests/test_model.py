from django.db import connection
from django.test import TestCase
from faker import Faker
from pendulum import DateTime

from portfolio import time_util
from portfolio.models import Transaction


class ModelTests(TestCase):

    fake = Faker()
    Faker.seed(0)

    def setUp(self):
        self.now = time_util.now()
        self.simple_txn, _ = Transaction.objects.get_or_create(
            symbol='a',
            price=1000,
            amount=100,
            transaction_time=time_util.now().subtract(days=10)
        )

    def test_int_date_time_field_python_type(self):
        self.assertIsInstance(self.simple_txn.create_time, DateTime)
        self.assertIsInstance(self.simple_txn.update_time, DateTime)

    def test_int_date_time_field_create_time_auto_now_add(self):
        self.assertAlmostEqual(self.now.int_timestamp, self.simple_txn.create_time.int_timestamp, delta=10)

        old = self.simple_txn.create_time
        self.simple_txn.symbol = 'b'
        self.simple_txn.save()
        self.assertEqual(old, self.simple_txn.create_time)

    def test_int_date_time_field_queryset(self):
        self.assertTrue(
            Transaction.objects.get(create_time=self.now),
            self.simple_txn
        )

    def test_int_date_time_field_create_time_raw_value(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT create_time FROM transaction_tab WHERE symbol = 'a'")
            rows = cursor.fetchall()
            self.assertTrue(len(rows) == 1)
            self.assertEqual(self.now.int_timestamp, rows[0][0])

    def test_int_date_time_field_update_time_set_value(self):
        now = time_util.now()
        self.simple_txn.update_time = time_util.now()

        self.assertEqual(now.int_timestamp, self.simple_txn.update_time.int_timestamp)
        self.assertIsInstance(self.simple_txn.update_time, DateTime)

    def test_int_date_time_field_update_time_value(self):
        current = time_util.now()

        self.assertIsNotNone(self.simple_txn.update_time)
        self.assertLess(self.simple_txn.update_time, current)

        self.simple_txn.symbol = 'b'
        self.simple_txn.save()

        self.assertGreaterEqual(self.simple_txn.update_time, current)

    def test_int_date_time_field_default_value(self):
        now = time_util.now()
        txn, _ = Transaction.objects.get_or_create(
            symbol='x',
            price=99,
            amount=3,
        )

        self.assertAlmostEqual(now.int_timestamp, txn.transaction_time.int_timestamp, delta=10)
