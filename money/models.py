from django.db import models

from common.models import IntDateTimeField


class Wallet(models.Model):
    class Meta:
        db_table = "wallet_tab"

    name = models.CharField(max_length=50, unique=True)
    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return self.name
