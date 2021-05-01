from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from portfolio import models


class PortfolioAdminSite(admin.AdminSite):
    site_title = settings.MODE.get_site_title_for('Homie')
    site_header = 'Homie'
    index_title = ''


portfolio_admin_site = PortfolioAdminSite(name='portfolio_admin')
portfolio_admin_site.register(User, UserAdmin)
portfolio_admin_site.register(Group, GroupAdmin)


@admin.register(models.Transaction, site=portfolio_admin_site)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'price', 'type')
    list_filter = ('type',)
    ordering = ('-create_time', 'symbol')


class TransactionInline(admin.TabularInline):
    model = models.Transaction
    fields = ('price', 'fee', 'subtotal', 'transaction_time')
    readonly_fields = ('subtotal',)


@admin.register(models.Holding, site=portfolio_admin_site)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'amount', 'total_value')
    ordering = ('symbol', )
    fields = ('symbol', 'amount', 'latest_price', 'total_value', 'update_time')
    readonly_fields = ('total_value',)
    inlines = (TransactionInline, )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

