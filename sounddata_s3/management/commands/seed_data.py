import csv
import boto3
import requests
from django.core.management.base import BaseCommand
from sounddata_s3.models import NYCSoundFile  # Replace with your actual model

# from django.conf import settings
from freesound import FreesoundClient
import os

# import environ
from dotenv import load_dotenv


class Command(BaseCommand):
    load_dotenv()
    help = (
        "Seed database with noise complaint data and sound files (limited to 10 rows)"
    )

    def handle(self, *args, **kwargs):
        local_csv_path = (
            "/Users/manavparikh/Desktop/Fall24/Software "
            "Engineering/Project/wed-fall24-team2/nyc_complaints_data.csv"
        )

        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SCRET_ACCESS_KEY = os.getenv("AWS_SCRET_ACCESS_KEY")

        print(AWS_ACCESS_KEY_ID)
        print(AWS_SCRET_ACCESS_KEY)

        # Initialize AWS S3
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SCRET_ACCESS_KEY,
        )

        # Initialize Freesound API client
        # FREESOUND_API_KEY = os.getenv('FREESOUND_API_KEY')
        FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")
        freesound_client = FreesoundClient()
        print(FREESOUND_API_KEY)

        freesound_client.set_token(FREESOUND_API_KEY, "token")

        # Read the CSV from S3 bucket
        # bucket_name = "nyc-soundscape-data"
        # file_key = "nyc_complaints_data.csv"

        with open(local_csv_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            # Limit to the first 10 rows
            for i, row in enumerate(reader):
                if i >= 50:
                    break

                unique_key = row["Unique Key"]
                latitude = row["Latitude"]
                longitude = row["Longitude"]
                sound_descriptor = row["Descriptor"]  # Adjust column name as needed

                # Uncomment this if you want to process sound files
                sound = self.get_sound_from_descriptor(
                    freesound_client, sound_descriptor
                )

                if sound:
                    sound_file_url = self.upload_sound_to_s3(
                        s3_client, sound, unique_key
                    )

                    # Save the data to the RDS database using Django ORM
                    NYCSoundFile.objects.create(  # Replace with your actual model
                        unique_key=unique_key,
                        latitude=latitude,
                        longitude=longitude,
                        sound_file_url=sound_file_url,
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Processed row "
                            f"{i + 1}: {unique_key} and {sound_descriptor} - Sound URL: {sound}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No sound found for {sound_descriptor}")
                    )

        # obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        # csv_data = obj['Body'].read().decode('utf-8').splitlines()

        # reader = csv.DictReader(csv_data)

        # #Limit to the first 10 rows
        # for i, row in enumerate(reader):
        #     if i >= 1:
        #         break

        #     unique_key = row['Unique Key']
        #     latitude = row['Latitude']
        #     longitude = row['Longitude']
        #     sound_descriptor = row['Descriptor']  # Adjust column name as needed

        #     # Fetch a sound file from Freesound based on the descriptor
        #     sound = self.get_sound_from_descriptor(freesound_client, sound_descriptor)

        #     if sound:
        #         sound_file_url = self.upload_sound_to_s3(s3_client, sound, unique_key)

        #         # Save the data to the RDS database using Django ORM
        #         NYCSoundFile.objects.create(  # Replace with your actual model
        #             unique_key=unique_key,
        #             latitude=latitude,
        #             longitude=longitude,
        #             sound_file_url=sound_file_url
        #         )

        # self.stdout.write(self.style.
        # SUCCESS(f"Processed row {i+1}: {unique_key} and {sound_descriptor} - Sound URL: {sound}"))

        #     else:
        #         self.stdout.write(self.style.WARNING(f"No sound found for {sound_descriptor}"))

    def get_sound_from_descriptor(self, client, descriptor):
        try:
            # Fetch sounds related to the descriptor from Freesound
            results = client.text_search(
                query=descriptor, fields="id,name,previews,duration"
            )

            # for sound in results:
            #     print(sound.duration)

            if results.count > 0:
                shortest_sound = min(results, key=lambda sound: sound.duration)
                print(shortest_sound.duration)
                print(shortest_sound.previews.preview_hq_mp3)
                return shortest_sound.previews.preview_hq_mp3
            else:
                self.stdout.write(
                    self.style.WARNING(f"No sounds found for {descriptor}")
                )
                return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching sound: {str(e)}"))
            return None

    def upload_sound_to_s3(self, client, sound_url, unique_key):
        AWS_S3_BUCKET_NAME = "nyc-soundscape-sound-files"
        try:
            response = requests.get(sound_url)
            sound_data = response.content
            sound_filename = f"{unique_key}.mp3"
            client.put_object(
                Bucket=AWS_S3_BUCKET_NAME,
                Key=sound_filename,
                Body=sound_data,
                ContentType="audio/mpeg",
            )
            s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{sound_filename}"
            return s3_url
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error uploading sound to S3: {str(e)}")
            )
            return None
