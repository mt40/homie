from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from pendulum import DateTime

from portfolio import time_util
from portfolio.const import TransactionType


def _parse_timestamp_to_datetime(value: int) -> DateTime:
    try:
        return time_util.from_unix_timestamp(value)
    except TypeError as err:
        raise ValidationError(str(err))


class IntDateTimeField(models.PositiveIntegerField):
    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def from_db_value(self, value, expression, connection) -> Optional[DateTime]:
        if value is None:
            return value
        return _parse_timestamp_to_datetime(value)

    def to_python(self, value):
        if value is None or isinstance(value, DateTime):
            return value
        return _parse_timestamp_to_datetime(value)

    def get_prep_value(self, value: DateTime):
        if isinstance(value, int) or value is None:  # already a timestamp
            return value

        return value.int_timestamp

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            now = time_util.now()
            setattr(model_instance, self.attname, now)
            return now

        return super().pre_save(model_instance, add)


class Transaction(models.Model):
    class Meta:
        db_table = "transaction_tab"

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

    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} x {self.symbol}"

    @property
    def subtotal(self) -> int:
        """Final cost of this transaction (including fees)"""
        return self.price * self.amount + self.fee

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        holding, _ = Holding.objects.get_or_create(symbol=self.symbol)
        holding.update_from_transaction(self)


class Holding(models.Model):
    """
    Represents the stocks that we are holding for each symbol.
    """

    class Meta:
        db_table = "holding_tab"
        indexes = (models.Index(fields=('symbol',), name='idx_symbol'),)

    symbol = models.CharField(max_length=50, unique=True)
    amount = models.PositiveIntegerField(default=0)
    latest_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="latest known price of this symbol in vnd"
    )

    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    @property
    def total_value(self) -> int:
        return self.amount * self.latest_price

    def update_from_transaction(self, txn: Transaction):
        if txn.symbol != self.symbol:
            return

        if txn.type == TransactionType.SELL:
            self.amount -= txn.amount
        else:
            self.amount += txn.amount
        self.latest_price = txn.price
        self.save()
