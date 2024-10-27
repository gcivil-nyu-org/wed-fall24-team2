import boto3
from django.conf import settings
from django.http import JsonResponse
from .forms import SoundFileUploadForm
from .models import SoundFileUser
from datetime import datetime


s3 = boto3.client('s3', 
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, 
                  region_name=settings.AWS_S3_REGION_NAME)

def upload_sound_file(request):
    if request.method == 'POST':
        form = SoundFileUploadForm(request.POST, request.FILES)
        print("here")
        if form.is_valid():
            user_name = form.cleaned_data['username']
            sound_file = request.FILES['sound_file']
            latitude = form.cleaned_data['latitude']
            sound_descriptor = form.cleaned_data['sound_descriptor']
            longitude = form.cleaned_data['longitude']

            # Generate S3 file path
            print("s3?")
            try:
                # Upload file to S3
                # s3.upload_fileobj(sound_file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)
                print("inside s3?")
                sound_data = sound_file.read()
                #s3_file_name = f"user_sounds/{user_name}_{sound_file.name}"
                s3_file_name = f"user_sounds/{user_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{sound_file.name}"

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
                    longitude=longitude
                )

                print("rds you done?")
                return JsonResponse({'message': 'Sound uploaded successfully'}, status=200)

            except Exception as e:
                return JsonResponse({'error': f'Error uploading to S3: {str(e)}'}, status=500)

        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def sounds_at_location(request, lat, lng):
    if request.method == 'GET':
        sounds = SoundFileUser.objects.filter(latitude=lat, longitude=lng)
        sound_list = [
            {
                'user_name': sound.user_name,
                'sound_descriptor': sound.sound_descriptor,
                'sound_name': sound.s3_file_name,
                'listen_link': f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{sound.s3_file_name}"
            }
            for sound in sounds
        ]
        return JsonResponse({'sounds': sound_list}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


