from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.urls import path

from money import models as money_models
from portfolio import models as portfolio_models, finance_util, views as portfolio_views
from portfolio.apps import PortfolioConfig


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
                f'{PortfolioConfig.name}/calculator-result/<int:result>',
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


@admin.register(portfolio_models.Transaction, site=homie_admin_site)
class TransactionAdmin(admin.ModelAdmin):
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
    readonly_fields = ('id', 'create_time', 'update_time')


class TransactionInline(admin.TabularInline):
    model = portfolio_models.Transaction
    fields = ('price', 'fee', 'subtotal', 'transaction_time')
    readonly_fields = ('subtotal',)


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
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', 'update_time')



