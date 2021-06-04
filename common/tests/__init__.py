from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User

from admin_site.management.commands import init_db


class BaseTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()

        # login to admin site so we can test admin views
        self.admin = User.objects.create_superuser(username='admin', password='123')
        self.client.login(username='admin', password='123')


class WithFakeData:
    def setUp(self) -> None:
        super().setUp()
        call_command(init_db.Command())