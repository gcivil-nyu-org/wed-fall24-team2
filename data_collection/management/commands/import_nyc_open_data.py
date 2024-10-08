from django.core.management.base import BaseCommand
import csv
from data_collection.models import NYCIncidentData
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports NYC incident data from a CSV file'

    def add_arguments(self, parser):
        # Adding the CSV file as an argument
        parser.add_argument('csv_file', type=str, help='The CSV file to import data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Set a limit for the number of rows to import (in this case 1000)
        row_limit = 1000

        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                count = 0
                for row in reader:
                    # Convert datetime strings to datetime objects
                    created_date = datetime.strptime(row['Created Date'], "%m/%d/%Y %I:%M:%S %p") if row['Created Date'] else None
                    closed_date = datetime.strptime(row['Closed Date'], "%m/%d/%Y %I:%M:%S %p") if row['Closed Date'] else None

                    # Create a new NYCIncidentData record
                    NYCIncidentData.objects.create(
                        unique_key=row['Unique Key'],
                        created_date=created_date,
                        closed_date=closed_date,
                        complaint_type=row['Complaint Type'],
                        location_type=row.get('Location Type', None),
                        incident_zip=row.get('Incident Zip', None),
                        incident_address=row.get('Incident Address', None),
                        city=row['City'],
                        status=row['Status'],
                        resolution_description=row.get('Resolution Description', None),
                        borough=row['Borough'],
                        latitude=float(row['Latitude']) if row['Latitude'] else None,
                        longitude=float(row['Longitude']) if row['Longitude'] else None,
                    )

                    count += 1
                    if count % 100 == 0:
                        self.stdout.write(self.style.NOTICE(f'{count} records imported...'))

                    # Stop after 1000 rows
                    if count >= row_limit:
                        self.stdout.write(self.style.SUCCESS(f'Stopped after importing {row_limit} rows for testing purposes.'))
                        break

                if count < row_limit:
                    self.stdout.write(self.style.SUCCESS(f'Data import completed successfully! Total records imported: {count}'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('The specified CSV file does not exist.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))

#todo  run this script using data in S3 as source