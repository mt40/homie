from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib.humanize.templatetags.humanize import intword
from django.urls import path
from django.utils.html import format_html

from money import models as money_models
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
    ordering = ('symbol', )
    fields = ('symbol', 'amount', 'latest_price', 'total_value', 'update_time')
    readonly_fields = ('total_value',)
    inlines = (TransactionInline, )

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
    list_filter = ('group', )


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


@admin.register(money_models.Budget, site=homie_admin_site)
class BudgetAdmin(BaseModelAdmin):
    ordering = ('expense_group', )
    list_display = ('expense_group', '_budget_limit', '_budget_limit_status')

    readonly_fields = ('_budget_limit_status', )
    fields = ('id', 'expense_group', 'limit', '_budget_limit_status')

    @admin.display(description='Status')
    def _budget_limit_status(self, budget: money_models.Budget) -> str:
        percent = budget.get_current_percent()
        bg = "bg-danger" if percent >= 100 else ""

        return format_html(
            f"""
            <div class="progress">
              <div class="progress-bar {bg}" role="progressbar" 
              style="width: {percent}%" 
              aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100">
              {intword(percent)}%
              </div>
            </div>
            """
        )

    @admin.display(description='Limit')
    def _budget_limit(self, budget: money_models.Budget) -> str:
        return intword(budget.limit)





