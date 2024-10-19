from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', 
                password='admin0000'
            )
        self.stdout.write(self.style.SUCCESS('Superuser has been created'))

