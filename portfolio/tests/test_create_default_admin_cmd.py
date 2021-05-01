import os
from io import StringIO
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from portfolio.management.commands import create_default_admin


class CreateDefaultAdminTest(TestCase):
    def setUp(self):
        self.command = create_default_admin.Command()

    @patch.object(settings, 'DEFAULT_ADMIN_PASSWORD', None)
    def test_without_password(self):
        self.assertRaises(ValueError, lambda: call_command(self.command))

    def test_created_user(self):
        call_command(self.command)
        user = User.objects.get(username=settings.DEFAULT_ADMIN_USERNAME)
        self.assertTrue(user.check_password('123'))

    def test_command_output(self):
        out = StringIO()
        call_command(self.command, stdout=out)
        self.assertIn(settings.DEFAULT_ADMIN_USERNAME, out.getvalue())
