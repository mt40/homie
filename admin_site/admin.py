from functools import reduce
from typing import List, Tuple

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.humanize.templatetags.humanize import intword
from django.template.loader import get_template
from django.urls import path
from django_admin_inline_paginator.admin import TabularInlinePaginated

from common import datetime_util, ml_util
from money import models as money_models
from money.models import Expense, ExpenseGroup, Budget, Income
from portfolio import models as portfolio_models, finance_util, views as portfolio_views
from portfolio.apps import PortfolioConfig


class HomieAdminSite(admin.AdminSite):
    site_title = settings.MODE.get_site_title_for('Homie')
    site_header = 'Homie'
    index_title = ''
    enable_nav_sidebar = False

    def get_urls(self):
        """
        Urls here can be reversed with namespace "homie_admin"
        """
        extra_urls = [
            path(
                f'{PortfolioConfig.name}/calculator',
                self.admin_view(
                    portfolio_views.CalculatorView.as_view()
                ),
                name="calculator"
            ),
            path(
                f'{PortfolioConfig.name}/calculator-result/'
                f'<int:fund>/'
                f'<int:risking_cash>/'
                f'<str:stop_loss_percent>/'
                f'<int:suggested_buy_amount>/'
                f'<int:total_buy_value>/'
                f'<str:suggested_sell_prices>/',
                self.admin_view(
                    portfolio_views.CalculatorResultView.as_view()
                ),
                name="calculator_result"
            ),
        ]
        return extra_urls + super().get_urls()

    def app_index(self, request, app_label, extra_context=None):
        return super().app_index(request, app_label, extra_context={
            'net_worth': finance_util.get_net_worth(),
            'pinned_models': [
                model_cls._meta.object_name
                for model_cls in (Budget, Expense, Income)
            ]
        })


homie_admin_site = HomieAdminSite(name='homie_admin')
homie_admin_site.register(User, UserAdmin)
homie_admin_site.register(Group, GroupAdmin)

@admin.register(LogEntry, site=homie_admin_site)
class LogEntryAdmin(admin.ModelAdmin):
    pass


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    # disable the default delete action and hide all select boxes
    actions = None

    view_on_site = True

    def get_readonly_fields(self, request, obj=None):
        return (
            *super().get_readonly_fields(request, obj),
            'id', 'create_time', 'update_time'
        )


@admin.register(portfolio_models.Transaction, site=homie_admin_site)
class TransactionAdmin(BaseModelAdmin):
    list_display = ('symbol', 'price', 'type')
    list_filter = ('type',)
    ordering = ('-create_time', 'symbol')
    fields = ('id', 'symbol',
              'type',
              'price',
              'amount',
              'fee',
              'transaction_time',
              'create_time',
              'update_time',)


class TransactionInline(TabularInlinePaginated):
    model = portfolio_models.Transaction
    fields = ('price', 'fee', 'subtotal', 'transaction_time')
    readonly_fields = ('subtotal',)
    per_page = 10
    show_change_link = True


@admin.register(portfolio_models.Holding, site=homie_admin_site)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'amount', 'total_value')
    ordering = ('symbol',)
    fields = ('symbol', 'amount', 'latest_price', 'total_value', 'update_time')
    readonly_fields = ('total_value',)
    inlines = (TransactionInline,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(amount__gt=0)


@admin.register(money_models.Wallet, site=homie_admin_site)
class WalletAdmin(BaseModelAdmin):
    search_fields = ('name', )


class IncomeCategoryInline(admin.TabularInline):
    model = money_models.IncomeCategory
    fields = ('name',)
    readonly_fields = ('name',)
    extra = 0
    show_change_link = True


@admin.register(money_models.IncomeGroup, site=homie_admin_site)
class IncomeGroupAdmin(BaseModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (IncomeCategoryInline,)


@admin.register(money_models.IncomeCategory, site=homie_admin_site)
class IncomeCategoryAdmin(BaseModelAdmin):
    ordering = ('group', 'name')
    search_fields = ('name',)

    list_display = ('group', 'name')
    list_filter = ('group',)


@admin.register(money_models.Income, site=homie_admin_site)
class IncomeAdmin(BaseModelAdmin):
    ordering = ('-receive_date', 'category', 'name')
    search_fields = ('category', 'name')
    date_hierarchy = 'receive_date'

    list_display = ('category', 'name', 'value', 'receive_date')
    list_filter = ('wallet', 'category')


class ExpenseCategoryInline(IncomeCategoryInline):
    model = money_models.ExpenseCategory


@admin.register(money_models.ExpenseGroup, site=homie_admin_site)
class ExpenseGroupAdmin(IncomeGroupAdmin):
    inlines = (ExpenseCategoryInline,)


@admin.register(money_models.ExpenseCategory, site=homie_admin_site)
class ExpenseCategoryAdmin(IncomeCategoryAdmin):
    search_fields = ('name', )


@admin.register(money_models.Expense, site=homie_admin_site)
class ExpenseAdmin(IncomeAdmin):
    ordering = ('-pay_date', 'category', 'name')
    list_display = ('category', 'name', 'value', 'pay_date')
    date_hierarchy = 'pay_date'
    autocomplete_fields = ('wallet', 'category')
    fields = (
        'id',
        'wallet',
        'category',
        'name',
        'value',
        'pay_date',
        '_budget_limit_status',
        'create_time',
        'update_time',
    )
    list_select_related = True

    @admin.display(description='Budget')
    def _budget_limit_status(self, expense: money_models.Expense) -> str:
        budget = expense.category.group.budget
        return get_template('admin/budget_limit_status.html').render(
            context={
                'budget': budget,
                'show_label': True,
            }
        )

    def get_readonly_fields(self, request, obj=None):
        return (
            *super().get_readonly_fields(request, obj),
            '_budget_limit_status',
        )


def _get_x_labels() -> List[str]:
    # labels on x axis
    # we only show important days
    important_days = (
        datetime_util.first_date_current_month(),
        datetime_util.today(),
        datetime_util.last_date_current_month(),
    )
    return [
        date.strftime('%d/%m') if date in important_days else ''
        for date in datetime_util.get_date_iterator(
            datetime_util.first_date_current_month(),
            datetime_util.last_date_current_month()
        )
    ]


def _get_current_accumulated_expenses(group: ExpenseGroup) -> List[int]:
    """
    Returns a list of accumulated expense. The i-th element is the expense
    from day 1 of this month until day i-th.
    """

    expense_til_today = []
    for date in datetime_util.get_date_iterator(
        datetime_util.first_date_current_month(),
        datetime_util.today()
    ):
        expense = sum([
            ex.value
            for ex in Expense.get_expenses_in(
                start_date=date, end_date=date
            ).filter(category__group=group)
        ])
        expense_til_today.append(
            expense
            if len(expense_til_today) == 0
            else expense_til_today[-1] + expense
        )

    return expense_til_today


def _get_y_values(group: ExpenseGroup) -> Tuple[List[int], int]:
    """
    Returns accumulated expense for each day of this month and
    the index of the entry for today.
    """

    current_daily_acc_expenses = _get_current_accumulated_expenses(group)
    expense_projections = ml_util.expense_projection(
        current_daily_acc_expenses,
        project_for=range(
            len(current_daily_acc_expenses) + 1,
            datetime_util.last_date_current_month().day + 1
        )
    )

    return current_daily_acc_expenses + expense_projections, len(current_daily_acc_expenses) - 1


@admin.register(money_models.Budget, site=homie_admin_site)
class BudgetAdmin(BaseModelAdmin):
    ordering = ('expense_group',)
    list_display = ('expense_group', '_budget_limit', '_budget_limit_status')
    autocomplete_fields = ('expense_group', )
    fields = (
        'id',
        'expense_group',
        'limit',
        '_budget_limit_status',
        '_budget_projection',
        'create_time',
        'update_time',
    )

    def get_readonly_fields(self, request, obj=None):
        return (
            *super().get_readonly_fields(request, obj),
            '_budget_limit_status',
            '_budget_projection',
        )

    @admin.display(description='Status')
    def _budget_limit_status(self, budget: money_models.Budget) -> str:
        return get_template('admin/budget_limit_status.html').render(
            context={'budget': budget}
        )

    @admin.display(description='Limit')
    def _budget_limit(self, budget: money_models.Budget) -> str:
        return intword(budget.limit)

    @admin.display(description='Projection')
    def _budget_projection(self, budget: money_models.Budget) -> str:
        y_values, today_index = _get_y_values(budget.expense_group)
        return get_template('admin/budget_projection.html').render(
            context={
                'x_labels': _get_x_labels(),
                'y_values': y_values,
                'budget': budget,
                'current_day_x_index': today_index,
            }
        )
