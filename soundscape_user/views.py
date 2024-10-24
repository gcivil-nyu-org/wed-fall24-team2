import boto3
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import SoundFileUploadForm
from .models import SoundFileUser

s3 = boto3.client('s3', 
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, 
                  region_name=settings.AWS_S3_REGION_NAME)

def upload_sound_file(request):
    if request.method == 'POST':
        form = SoundFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sound_file = request.FILES['sound_file']
            sound_descriptor = form.cleaned_data['sound_descriptor']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']

            # Upload file to S3
            s3_file_name = f'user_sounds/{sound_file.name}'
            s3.upload_fileobj(sound_file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)

            # Save the file info in the RDS (your Django DB)
            SoundFileUser.objects.create(
                user=request.user,
                sound_descriptor=sound_descriptor,
                s3_file_name=s3_file_name,
                latitude=latitude,
                longitude=longitude
            )
            return redirect('success_page')  # Redirect to a success page
    else:
        form = SoundFileUploadForm()
    
    return render(request, 'soundfiles/upload.html', {'form': form})
