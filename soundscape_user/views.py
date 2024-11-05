import boto3
import json
from django.conf import settings
from django.http import JsonResponse
from .forms import SoundFileUploadForm
from .models import SoundFileUser
from datetime import datetime


s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


def upload_sound_file(request):
    if request.method == "POST":
        form = SoundFileUploadForm(request.POST, request.FILES)
        print("here")
        if form.is_valid():
            user_name = form.cleaned_data["username"]
            sound_file = request.FILES["sound_file"]
            print(sound_file.size)
            if sound_file.size > 3 * 1024 * 1024:  # 3 MB
                return JsonResponse(
                    {"error": "Please limit the sound file size to 3 MB"}, status=400
                )

            latitude = form.cleaned_data["latitude"]
            sound_descriptor = form.cleaned_data["sound_descriptor"]
            longitude = form.cleaned_data["longitude"]

            # Generate S3 file path
            print("s3?")
            try:
                # Upload file to S3
                # s3.upload_fileobj(sound_file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)
                print("inside s3?")
                sound_data = sound_file.read()
                # s3_file_name = f"user_sounds/{user_name}_{sound_file.name}"
                s3_file_name = (
                    f"user_sounds/{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    f"_{sound_file.name}"
                )

                s3.put_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=s3_file_name,
                    Body=sound_data,
                    ContentType=sound_file.content_type,
                )

                print("was this success?")

                print("rds here we come?")

                # Save metadata in RDS
                SoundFileUser.objects.create(
                    user_name=user_name,
                    sound_descriptor=sound_descriptor,
                    s3_file_name=s3_file_name,
                    latitude=latitude,
                    longitude=longitude,
                )

                print("rds you done?")
                return JsonResponse(
                    {"message": "Sound uploaded successfully"}, status=200
                )

            except Exception as e:
                return JsonResponse(
                    {"error": f"Error uploading to S3: {str(e)}"}, status=500
                )

        else:
            return JsonResponse({"errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def sounds_at_location(request, lat, lng):
    if request.method == "GET":
        sounds = SoundFileUser.objects.filter(latitude=lat, longitude=lng)
        sound_list = [
            {
                "user_name": sound.user_name,
                "sound_descriptor": sound.sound_descriptor,
                "sound_name": sound.s3_file_name,
                "listen_link": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3"
                f".{settings.AWS_S3_REGION_NAME}.amazonaws.com/{sound.s3_file_name}",
            }
            for sound in sounds
        ]
        return JsonResponse({"sounds": sound_list}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def check_file_exists_in_s3(key):
    try:
        s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
        )
        return True
    except Exception as e:
        print(f"Cannot find file {key}: {e}")
        return False


def delete_sound_file(request):
    if request.method == "POST":
        sound = json.loads(request.body)

        if check_file_exists_in_s3(sound["sound_name"]):
            try:
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=sound["sound_name"],
                )
            except Exception as e:
                return JsonResponse(
                    {"error": f"Error deleting in S3: {str(e)}"}, status=500
                )
        else:
            print("Cannot find file in s3, delete metadata from RDS anyway")

        SoundFileUser.objects.filter(
            user_name=sound["user_name"],
            s3_file_name=sound["sound_name"],
        ).delete()

        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
