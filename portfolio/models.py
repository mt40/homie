from django.db import models
from django.utils.functional import cached_property

from common.models import IntDateTimeField
from portfolio import time_util, const
from portfolio.const import TransactionType, DEPOSIT_SYMBOL


class Transaction(models.Model):
    class Meta:
        db_table = "transaction_tab"
        indexes = (models.Index(fields=('symbol',), name='idx_symbol'),)

    # if type is DEPOSIT, symbol is const.DEPOSIT_SYMBOL
    symbol = models.CharField(max_length=50)
    type = models.PositiveSmallIntegerField(
        choices=TransactionType.choices,
        default=TransactionType.BUY
    )
    price = models.PositiveIntegerField(help_text="in vnd")
    amount = models.PositiveIntegerField()
    fee = models.PositiveIntegerField(default=0, help_text="in vnd")
    transaction_time = IntDateTimeField(default=time_util.now)

    # reference to holding of this symbol
    # this is nullable and we will assign a value once this instance is saved
    holding = models.ForeignKey('Holding', on_delete=models.PROTECT, null=True)

    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} x {self.symbol}"

    @property
    def subtotal(self) -> int:
        """Final cost of this transaction (including fees)"""
        return self.price * self.amount + self.fee

    def save(self, *args, **kwargs):
        holding, _ = Holding.objects.get_or_create(symbol=self.symbol)
        self.holding = holding
        super().save(*args, **kwargs)

        # we need to adjust our available fund
        # e.g. if we buy something, our fund should decrease
        if self.symbol != DEPOSIT_SYMBOL:
            Transaction.objects.create(
                symbol=DEPOSIT_SYMBOL,
                type=(
                    TransactionType.BUY
                    if self.type == TransactionType.SELL
                    else TransactionType.SELL
                ),
                price=self.subtotal,
                amount=1,
            )

        holding.refresh_amount_and_price()


class Holding(models.Model):
    """
    Represents the stocks that we are holding for each symbol.
    """

    class Meta:
        db_table = "holding_tab"

    symbol = models.CharField(max_length=50, unique=True)
    amount = models.PositiveIntegerField(
        default=0,
        help_text=(
            "number of shares of this symbol,"
            "ignored for FUND"
        )
    )
    latest_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "latest known price of this symbol in vnd,"
            "ignored for FUND"
        )
    )

    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    @property
    def total_value(self) -> int:
        if self.symbol == const.DEPOSIT_SYMBOL:
            return self.get_fund()
        return self.amount * self.latest_price

    def refresh_amount_and_price(self):
        if self.symbol == const.DEPOSIT_SYMBOL:
            self.amount = 1
            self.latest_price = 0
        else:
            transactions = Transaction.objects.filter(symbol=self.symbol).order_by(
                'transaction_time').all()
            self.amount = 0
            for txn in transactions:
                if txn.type == TransactionType.SELL:
                    self.amount -= txn.amount
                else:
                    self.amount += txn.amount
                self.latest_price = txn.price

        self.save()

    @staticmethod
    def get_fund() -> int:
        """
        Returns the available fund.
        """
        transactions = Transaction.objects.filter(symbol=const.DEPOSIT_SYMBOL)
        total = 0
        for txn in transactions:
            if txn.type == TransactionType.SELL:
                total -= txn.subtotal
            else:
                total += txn.subtotal
        return total
