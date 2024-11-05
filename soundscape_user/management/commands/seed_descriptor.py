from django.core.management.base import BaseCommand
from soundscape_user.models import SoundDescriptor


class Command(BaseCommand):
    help = "Add a new sound descriptor to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "descriptor",
            type=str,
            help="The sound descriptor to add to the database",
        )

    def handle(self, *args, **options):
        descriptor = options["descriptor"]
        # Check if descriptor already exists
        if SoundDescriptor.objects.filter(descriptor=descriptor).exists():
            self.stdout.write(
                self.style.WARNING(f'Sound descriptor "{descriptor}" already exists.')
            )
        else:
            # Create and save the new descriptor
            SoundDescriptor.objects.create(descriptor=descriptor)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added descriptor "{descriptor}".')
            )
