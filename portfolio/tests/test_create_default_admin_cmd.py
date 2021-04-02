import os
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase


_COMMAND_NAME = 'create_default_admin'


class CreateDefaultAdminTest(TestCase):
    def setUp(self):
        os.environ['DEFAULT_ADMIN_USERNAME'] = 'john'
        os.environ['DEFAULT_ADMIN_PASSWORD'] = '123'

    def test_without_password(self):
        os.environ.pop('DEFAULT_ADMIN_PASSWORD')
        self.assertRaises(KeyError, lambda: call_command(_COMMAND_NAME))

    def test_created_user(self):
        call_command(_COMMAND_NAME)
        user = User.objects.get(username='john')
        self.assertTrue(user.check_password('123'))

    def test_command_output(self):
        out = StringIO()
        call_command(_COMMAND_NAME, stdout=out)
        self.assertIn('john', out.getvalue())
