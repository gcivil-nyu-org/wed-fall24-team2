from django.core.management.base import BaseCommand
import csv
from data_collection.models import NYCIncidentData
from datetime import datetime
import os
import boto3
from django.conf import settings
from django.utils.timezone import make_aware
import pytz


class Command(BaseCommand):
    help = (
        "Imports NYC incident data from a CSV file or S3, depending on the environment"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            nargs="?",
            type=str,
            default=None,
            help="The CSV file to import data from",
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"] or "/tmp/nyc_complaints_data.csv"

        # Testing
        row_limit = 1000

        # Check if we're running in production (DEBUG=False)
        # is_production = (
        #     not settings.DEBUG
        # )
        # hardcode as True; testing production behavior

        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.NOTICE("CSV file not found locally. Checking S3...")
            )
            csv_file = self.download_from_s3(csv_file)

        if csv_file and os.path.exists(csv_file):
            self.load_dataset(csv_file, row_limit)
        else:
            self.stderr.write(
                self.style.ERROR("CSV file is not available locally or on S3.")
            )

    def download_from_s3(self, csv_file):
        s3_bucket_name = "nyc-soundscape-data"
        s3_file_key = "nyc_complaints_data.csv"

        s3 = boto3.client("s3")

        try:
            self.stdout.write(
                self.style.NOTICE(
                    f"Downloading {s3_file_key} from S3 bucket {s3_bucket_name}..."
                )
            )
            s3.download_file(s3_bucket_name, s3_file_key, csv_file)
            self.stdout.write(
                self.style.SUCCESS(f"CSV file downloaded and saved to {csv_file}.")
            )
            return csv_file
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error downloading file from S3: {e}"))
            return None

    def load_dataset(self, csv_file, row_limit):
        try:
            with open(csv_file, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                count = 0
                for row in reader:
                    created_date = (
                        self.convert_to_timezone_aware(row["Created Date"])
                        if row["Created Date"]
                        else None
                    )
                    closed_date = (
                        self.convert_to_timezone_aware(row["Closed Date"])
                        if row["Closed Date"]
                        else None
                    )

                    NYCIncidentData.objects.create(
                        unique_key=row["Unique Key"],
                        created_date=created_date,
                        closed_date=closed_date,
                        complaint_type=row["Complaint Type"],
                        location_type=row.get("Location Type", None),
                        incident_zip=row.get("Incident Zip", None),
                        incident_address=row.get("Incident Address", None),
                        city=row["City"],
                        status=row["Status"],
                        resolution_description=row.get("Resolution Description", None),
                        borough=row["Borough"],
                        latitude=float(row["Latitude"]) if row["Latitude"] else None,
                        longitude=float(row["Longitude"]) if row["Longitude"] else None,
                    )

                    count += 1
                    if count % 100 == 0:
                        self.stdout.write(
                            self.style.NOTICE(f"{count} records imported...")
                        )

                    # Stop after the specified row_limit
                    if count >= row_limit:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Stopped after importing {row_limit} rows for testing purposes."
                            )
                        )
                        break

                if count < row_limit:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Data import completed successfully! Total records imported: {count}"
                        )
                    )

        except FileNotFoundError:
            self.stderr.write(
                self.style.ERROR("The specified CSV file does not exist.")
            )
        except ValueError as ve:
            self.stderr.write(self.style.ERROR(f"Data parsing error: {ve}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

    def convert_to_timezone_aware(self, date_string):
        naive_datetime = datetime.strptime(date_string, "%m/%d/%Y %I:%M:%S %p")
        return make_aware(
            naive_datetime, pytz.timezone("America/New_York")
        )  # Adjust the time zone as per our needs
