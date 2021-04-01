from django.db import models


class TransactionType(models.IntegerChoices):
    BUY = 1
    SELL = 2

    # add funds
    DEPOSIT = 3
