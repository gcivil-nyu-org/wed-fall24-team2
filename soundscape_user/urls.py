from django.urls import path
from .views import upload_sound_file

urlpatterns = [
    path('upload/', upload_sound_file, name='upload_sound_file'),
]