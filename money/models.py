import datetime

from django.db import models

from common.models import IntDateTimeField, BaseModel
from portfolio import time_util


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
    receive_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.category}: {self.value}"


class ExpenseGroup(BaseModel):
    class Meta:
        db_table = "expense_group_tab"

    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return str(self.name)


class ExpenseCategory(BaseModel):
    class Meta:
        db_table = "expense_category_tab"
        verbose_name_plural = 'expense categories'

    group = models.ForeignKey(ExpenseGroup, on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return str(self.name)


class Expense(BaseModel):
    class Meta:
        db_table = "expense_tab"

    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, blank=False)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, blank=False)
    name = models.CharField(max_length=500, blank=True)
    value = models.PositiveIntegerField(blank=False)
    pay_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.category}: {self.value}"
