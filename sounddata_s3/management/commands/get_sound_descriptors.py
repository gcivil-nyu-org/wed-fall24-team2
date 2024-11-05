import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetch unique sound descriptors from the CSV file"

    def handle(self, *args, **kwargs):
        local_csv_path = (
            "/Users/manavparikh/Desktop/Fall24/Software Engineering/Project/wed-fall24-team2/nyc_complaints_data.csv"
        )
        unique_descriptors = set()

        with open(local_csv_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                descriptor = row.get("Descriptor")
                if descriptor:
                    unique_descriptors.add(descriptor)

        unique_descriptors_list = list(unique_descriptors)
        self.stdout.write(
            f"Unique Descriptors ({len(unique_descriptors_list)}): {unique_descriptors_list}"
        )
