import os

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Grant DB privileges for our app. This only works with Postgres!'

    def handle(self, *args, **options):
        app_user = os.environ['APP_DB_USER']

        with connection.cursor() as cursor:
            cursor.execute(
                "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES "
                f"IN SCHEMA public TO {app_user}"
            )
            cursor.execute(
                "GRANT SELECT, UPDATE ON ALL SEQUENCES "
                f"IN SCHEMA public TO {app_user}",
            )
