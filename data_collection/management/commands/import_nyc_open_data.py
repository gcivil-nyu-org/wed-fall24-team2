from django.core.management.base import BaseCommand
import csv
from data_collection.models import NYCIncidentData
from datetime import datetime
import os
import boto3
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports NYC incident data from a CSV file or S3, depending on the environment'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', nargs='?', type=str, default=None, help='The CSV file to import data from'
        )

    def handle(self, *args, **kwargs):
        # Check if data already exists
        if NYCIncidentData.objects.exists():
            self.stdout.write(self.style.SUCCESS('Data already exists. Skipping import.'))
            return

        csv_file = kwargs['csv_file']

        # Set a limit for the number of rows to import (in this case 1000)
        row_limit = 1000

        # Check if we're running in production (DEBUG=False)
        #testing rn
        is_production = True

        if is_production:
            self.stdout.write(self.style.NOTICE('Production environment detected. Downloading CSV from S3...'))
            csv_file = self.download_from_s3(csv_file)
        elif not csv_file or not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR('Please provide a valid CSV file for local import.'))
            return

        self.load_dataset(csv_file, row_limit, is_production)

    def download_from_s3(self, csv_file_key):
        s3_bucket_name = 'nyc-soundscape-data'
        local_tmp_file = '/tmp/nyc_complaints_data.csv'

        s3 = boto3.client('s3')

        if not csv_file_key:
            csv_file_key = 'nyc_complaints_data.csv'

        try:
            self.stdout.write(self.style.NOTICE(f'Downloading {csv_file_key} from S3 bucket {s3_bucket_name}...'))
            s3.download_file(s3_bucket_name, csv_file_key, local_tmp_file)
            self.stdout.write(self.style.SUCCESS('CSV download from S3 completed successfully.'))
            return local_tmp_file
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error downloading file from S3: {e}"))
            raise e

    def load_dataset(self, csv_file, row_limit, is_production):
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                count = 0
                for row in reader:
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

                    # Stop after the specified row_limit
                    if count >= row_limit:
                        self.stdout.write(self.style.SUCCESS(f'Stopped after importing {row_limit} rows for testing purposes.'))
                        break

                if count < row_limit:
                    self.stdout.write(self.style.SUCCESS(f'Data import completed successfully! Total records imported: {count}'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('The specified CSV file does not exist.'))
        except ValueError as ve:
            self.stderr.write(self.style.ERROR(f'Data parsing error: {ve}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
        finally:
            # Clean up the local file only if it was downloaded from S3
            if is_production and os.path.exists(csv_file) and '/tmp/' in csv_file:
                try:
                    os.remove(csv_file)
                    self.stdout.write(self.style.NOTICE(f'Temporary file {csv_file} removed successfully.'))
                except Exception as cleanup_error:
                    self.stderr.write(self.style.ERROR(f'Error cleaning up temporary file: {cleanup_error}'))
