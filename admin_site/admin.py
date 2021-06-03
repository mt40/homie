import datetime
from time import strftime
from typing import List, Tuple

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.humanize.templatetags.humanize import intword
from django.template.loader import get_template
from django.urls import path
from django.utils.html import format_html

from common import datetime_util
from money import models as money_models
from money.models import Expense
from portfolio import models as portfolio_models, finance_util, views as portfolio_views
from portfolio.apps import PortfolioConfig
from django_admin_inline_paginator.admin import TabularInlinePaginated


class HomieAdminSite(admin.AdminSite):
    site_title = settings.MODE.get_site_title_for('Homie')
    site_header = 'Homie'
    index_title = ''

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


homie_admin_site = HomieAdminSite(name='homie_admin')
homie_admin_site.register(User, UserAdmin)
homie_admin_site.register(Group, GroupAdmin)


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


@admin.register(portfolio_models.Holding, site=homie_admin_site)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'amount', 'total_value')
    ordering = ('symbol',)
    fields = ('symbol', 'amount', 'latest_price', 'total_value', 'update_time')
    readonly_fields = ('total_value',)
    inlines = (TransactionInline,)

    change_list_template = "admin/holding_changelist_template.html"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context={
            **(extra_context or {}),
            'net_worth': finance_util.get_net_worth()
        })


@admin.register(money_models.Wallet, site=homie_admin_site)
class WalletAdmin(BaseModelAdmin):
    pass


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
    pass


@admin.register(money_models.Expense, site=homie_admin_site)
class ExpenseAdmin(IncomeAdmin):
    ordering = ('-pay_date', 'category', 'name')
    list_display = ('category', 'name', 'value', 'pay_date')
    date_hierarchy = 'pay_date'


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


def _get_y_values() -> Tuple[List[int], int]:
    """
    Returns expense for each day of this month and
    the index of the entry for today.
    """

    # expense of each day until today
    expense_til_today = []
    for date in datetime_util.get_date_iterator(
        datetime_util.first_date_current_month(),
        datetime_util.today()
    ):
        expense = sum([
            ex.value
            for ex in Expense.get_expenses_in(
                start_date=date, end_date=date
            )
        ])
        expense_til_today.append(expense)

    # expense projection for the remaining days
    expense_projections = []
    for date in datetime_util.get_date_iterator(
        datetime_util.tmr(),
        datetime_util.last_date_current_month()
    ):
        projection = date.day * 1000 * 1000  # todo
        expense_projections.append(projection)

    return expense_til_today + expense_projections, len(expense_til_today) - 1


# testme
@admin.register(money_models.Budget, site=homie_admin_site)
class BudgetAdmin(BaseModelAdmin):
    ordering = ('expense_group',)
    list_display = ('expense_group', '_budget_limit', '_budget_limit_status')

    readonly_fields = ('_budget_limit_status', '_budget_projection')
    fields = ('id', 'expense_group', 'limit', '_budget_limit_status', '_budget_projection')

    @admin.display(description='Status')
    def _budget_limit_status(self, budget: money_models.Budget) -> str:
        return get_template('admin/budget_limit_status.html').render(
            context={
                'percent': budget.get_current_percent()
            }
        )

    @admin.display(description='Limit')
    def _budget_limit(self, budget: money_models.Budget) -> str:
        return intword(budget.limit)

    # todo:
    #  v- show all days data
    #  v- hide x/y values except first, today, and last day
    #  v- dash line for projection
    #  v- grad bg
    #  v- limit line
    #  - animation
    #  v- different colors for: first to today, today to limit, limit to last day
    @admin.display(description='Projection')
    def _budget_projection(self, budget: money_models.Budget) -> str:
        y_values, today_index = _get_y_values()
        return get_template('admin/budget_projection.html').render(
            context={
                'x_labels': _get_x_labels(),
                'y_values': y_values,
                'budget': budget,
                'current_day_x_index': today_index,
                'prediction': 10 * 1000 * 1000,
            }
        )
