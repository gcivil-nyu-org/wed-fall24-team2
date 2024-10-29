from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(
            username=os.environ["DJANGO_SUPERUSER_USERNAME"]
        ).exists():
            User.objects.create_superuser(
                username=os.environ["DJANGO_SUPERUSER_USERNAME"],
                password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
            )
            self.stdout.write(self.style.SUCCESS("Superuser admin has been created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser admin already exists"))
