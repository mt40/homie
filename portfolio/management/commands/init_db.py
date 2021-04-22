from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker
from pendulum import timezone

from portfolio.models import Transaction


class Command(BaseCommand):
    help = 'Insert some sample data into db to support dev'

    fake = Faker()
    Faker.seed(0)

    def handle(self, *args, **options):
        n_txn = 10
        for i in range(0, n_txn):
            buy = Transaction.objects.get_or_create(
                symbol=self.fake.tld(),
                price=self.fake.random.randint(2000, 30000),
                amount=self.fake.random.randint(100, 1000),
                fee=self.fake.random.randint(1000, 5000),
                transaction_time=self.fake.date_time_between(
                    start_date='-30d',
                    end_date='now',
                    tzinfo=timezone(settings.TIME_ZONE)
                ),
            )
        self.stdout.write(f'inserted {n_txn} transactions')
