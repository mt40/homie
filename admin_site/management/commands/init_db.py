from django.core.management.base import BaseCommand
from faker import Faker

from money.models import Wallet, IncomeGroup, IncomeCategory, Income
from portfolio import time_util
from portfolio.const import TransactionType, DEPOSIT_SYMBOL
from portfolio.models import Transaction, Holding


class Command(BaseCommand):
    help = 'Insert some sample data into db to support dev'

    fake = Faker()
    Faker.seed(0)

    def handle(self, *args, **options):
        self.init_portfolio()
        self.init_money()

    def init_portfolio(self):
        # add a few deposits
        Transaction.objects.get_or_create(
            symbol=DEPOSIT_SYMBOL,
            price=self.fake.random.randint(30000, 100000),
            amount=1,
            transaction_time=time_util.now().subtract(days=40),
        )
        Transaction.objects.get_or_create(
            symbol=DEPOSIT_SYMBOL,
            price=self.fake.random.randint(30000, 100000),
            amount=1,
            transaction_time=time_util.now().subtract(days=self.fake.pyint(0, 30)),
        )
        buys = [
            Transaction.objects.get_or_create(
                symbol=self.fake.tld().upper(),
                price=self.fake.random.randint(2000, 30000),
                amount=self.fake.random.randint(100, 1000),
                fee=self.fake.random.randint(1000, 5000),
                transaction_time=time_util.now().subtract(days=self.fake.pyint(0, 30)),
            )[0]
            for _ in range(0, 10)
        ]
        for buy in buys:
            for i in range(0, self.fake.random.randint(0, 2)):
                holding = Holding.objects.get(symbol=buy.symbol)
                if holding.amount > 0:
                    Transaction.objects.get_or_create(
                        symbol=buy.symbol,
                        type=TransactionType.SELL,
                        price=self.fake.pyint(2000, 30000),
                        amount=(
                            self.fake.pyint(1, holding.amount)
                        ),
                        fee=self.fake.pyint(1000, 5000),
                        transaction_time=min(
                            time_util.now(),
                            buy.transaction_time.add(days=self.fake.pyint(0, 10))
                        ),
                    )

    def init_money(self):
        Wallet.objects.get_or_create(name="Bank")
        Wallet.objects.get_or_create(name="Credit Card")
        wallets = Wallet.objects.all()

        food, _ = IncomeGroup.objects.get_or_create(name="Food")
        beauty, _ = IncomeGroup.objects.get_or_create(name="Beauty")

        IncomeCategory.objects.get_or_create(group=food, name='Drink')
        IncomeCategory.objects.get_or_create(group=food, name='Dinner')
        IncomeCategory.objects.get_or_create(group=beauty, name='Spa')

        for category in IncomeCategory.objects.all():
            for i in range(0, 5):
                Income.objects.get_or_create(
                    wallet=self.fake.random.choice(wallets),
                    category=category,
                    name=self.fake.sentence(nb_words=5),
                    value=self.fake.pyint(1000, 1000000),
                    receive_time=time_util.now().subtract(days=self.fake.pyint(0, 30)),
                )
