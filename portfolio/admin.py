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
