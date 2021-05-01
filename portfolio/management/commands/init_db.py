import pendulum
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker
from pendulum import timezone

from portfolio.const import TransactionType, DEPOSIT_SYMBOL
from portfolio.models import Transaction


class Command(BaseCommand):
    help = 'Insert some sample data into db to support dev'

    fake = Faker()
    Faker.seed(0)

    # testme
    def handle(self, *args, **options):
        Transaction.objects.get_or_create(
            symbol=DEPOSIT_SYMBOL,
            price=self.fake.random.randint(30000, 100000),
            amount=1,
            transaction_time=pendulum.now().subtract(days=40),
        )
        Transaction.objects.get_or_create(
            symbol=DEPOSIT_SYMBOL,
            price=self.fake.random.randint(30000, 100000),
            amount=1,
            transaction_time=self.fake.date_time_between(
                start_date='-30d',
                end_date='now',
                tzinfo=timezone(settings.TIME_ZONE)
            ),
        )

        for i in range(0, 10):
            buy = Transaction.objects.get_or_create(
                symbol=self.fake.tld().upper(),
                price=self.fake.random.randint(2000, 30000),
                amount=self.fake.random.randint(100, 1000),
                fee=self.fake.random.randint(1000, 5000),
                transaction_time=self.fake.date_time_between(
                    start_date='-30d',
                    end_date='now',
                    tzinfo=timezone(settings.TIME_ZONE)
                ),
            )
        buys = Transaction.objects.filter(type=TransactionType.BUY).all()
        for buy in buys:
            for i in range(0, self.fake.random.randint(0, 2)):
                Transaction.objects.get_or_create(
                    symbol=self.fake.tld().upper(),
                    type=TransactionType.SELL,
                    price=self.fake.random.randint(2000, 30000),
                    amount=self.fake.random.randint(1, buy.amount),
                    fee=self.fake.random.randint(1000, 5000),
                    transaction_time=self.fake.date_time_between_dates(
                        datetime_start=buy.transaction_time,  # todo
                        datetime_end=pendulum.now(),
                        tzinfo=timezone(settings.TIME_ZONE)
                    ),
                )
