from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if settings.DEFAULT_ADMIN_PASSWORD is None:
            raise ValueError('default admin password must be set')

        username = settings.DEFAULT_ADMIN_USERNAME
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=settings.DEFAULT_ADMIN_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully create admin user: {username}'))