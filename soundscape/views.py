from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import SignupForm
from chatroom.models import Chatroom

from sounddata_s3.models import NYCSoundFile
# from data_collection.models import NYCIncidentData

import os
import json


def homepage(request):
    sound_data = NYCSoundFile.objects.all()

    sound_data_list = []
    for sound in sound_data:
        sound_data_list.append(
            {
                "unique_key": sound.unique_key,
                "latitude": sound.latitude,
                "longitude": sound.longitude,
                "sound_file_url": sound.sound_file_url,
            }
        )

    sound_data_json = json.dumps(sound_data_list)

    return render(
        request,
        "soundscape/homepage.html",
        {
            "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
            "chatrooms": json.dumps(
                [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
            ),
            "username": request.user.username,
            "sound_data": sound_data_json,
        },
    )


def about(request):
    return render(request, "soundscape/about.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SignupForm()

    return render(request, "soundscape/signup.html", {"form": form})
