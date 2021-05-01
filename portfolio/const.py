from django.db import models


# symbol of all deposit transactions
DEPOSIT_SYMBOL = "FUND"


class TransactionType(models.IntegerChoices):
    BUY = 1
    SELL = 2

    # add funds
    DEPOSIT = 3


class Mode(models.TextChoices):
    LOCAL = 'local'
    TEST = 'test'
    LIVE = 'live'

    def get_site_title_for(self, prefix: str) -> str:
        if self == self.LIVE:
            return prefix
        return f"{prefix} ({self})"

