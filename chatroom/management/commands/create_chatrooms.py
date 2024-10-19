import csv
from django.core.management.base import BaseCommand
from chatroom.models import Chatroom

class Command(BaseCommand):
    help = 'Create chatrooms'

    def handle(self, *args, **kwargs):
        csv_file = './chatroom/management/commands/NYC_Neighborhoods.csv'

        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if not Chatroom.objects.filter(name=row['name']).exists():
                        Chatroom.objects.create(**row)
                        self.stdout.write(self.style.SUCCESS(f'Chatrooms {row["name"]} has been created'))

            self.stdout.write(self.style.SUCCESS('Chatrooms have been created'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The specified CSV file does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
