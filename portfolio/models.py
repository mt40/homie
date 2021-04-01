from django.db import models


class Transaction(models.Model):
    symbol: models.CharField()
    price: models.PositiveIntegerField()
    create_time: models.DateTimeField(auto_now_add=True)
    update_time: models.DateTimeField(auto_now=True)
