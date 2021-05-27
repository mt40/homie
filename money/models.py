from django.db import models

from common.models import IntDateTimeField, BaseModel


class Wallet(BaseModel):
    class Meta:
        db_table = "wallet_tab"

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class IncomeGroup(BaseModel):
    class Meta:
        db_table = "income_group_tab"

    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return str(self.name)


class IncomeCategory(BaseModel):
    class Meta:
        db_table = "income_category_tab"
        verbose_name_plural = 'income categories'

    group = models.ForeignKey(IncomeGroup, on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return str(self.name)


class Income(BaseModel):
    class Meta:
        db_table = "income_tab"

    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, blank=False)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=500, blank=True)
    value = models.PositiveIntegerField(blank=False)
    receive_time = IntDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}: {self.value}"
