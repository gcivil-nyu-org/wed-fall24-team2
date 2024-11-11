from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_sound_file, name="upload_sound_file"),
    path(
        "soundfiles_at_location/<str:lat>/<str:lng>/",
        views.sounds_at_location,
        name="sounds_at_location",
    ),
<<<<<<< HEAD
=======
    path(
        "soundfiles_for_user/<str:user_name>/",
        views.sounds_for_user,
        name="sounds_for_user",
    ),
>>>>>>> develop
    path("delete/", views.delete_sound_file, name="delete_sound_file"),
]
