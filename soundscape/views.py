from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import SignupForm
from chatroom.models import Chatroom

import requests

import os
import json


# def homepage(request):
#     sound_data = NYCSoundFile.objects.all()

#     sound_data_list = []
#     for sound in sound_data:
#         sound_data_list.append(
#             {
#                 "unique_key": sound.unique_key,
#                 "latitude": sound.latitude,
#                 "longitude": sound.longitude,
#                 "sound_file_url": sound.sound_file_url,
#             }
#         )

#     sound_data_json = json.dumps(sound_data_list)

#     return render(
#         request,
#         "soundscape/homepage.html",
#         {
#             "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
#             "chatrooms": json.dumps(
#                 [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
#             ),
#             "username": request.user.username,
#             "sound_data": sound_data_json,
#         },
#     )


def homepage(request):
    API_URL = "https://data.cityofnewyork.us/resource/hbc2-s6te.json"
    APP_TOKEN = os.environ.get("NYC_OPEN_DATA_APP_TOKEN")
    headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

    BATCH_SIZE = 1000  # Socrata's max limit per request
    TOTAL_ROWS = 2000
    all_data = []

    try:
        # Fetch data in parallel batches for efficiency
        batch_offsets = range(0, TOTAL_ROWS, BATCH_SIZE)

        for offset in batch_offsets:
            params = {
                "$limit": min(BATCH_SIZE, TOTAL_ROWS - offset),
                "$offset": offset,
            }

            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()

            batch_data = response.json()
            if not batch_data:
                break

            all_data.extend(batch_data)
            if len(batch_data) < params["$limit"]:
                break

        return render(
            request,
            "soundscape/homepage.html",
            {
                "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
                "chatrooms": json.dumps(
                    [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
                ),
                "username": request.user.username,
                "sound_data": json.dumps(all_data),
            },
        )

    except requests.RequestException as e:
        return render(
            request,
            "soundscape/homepage.html",
            {
                "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
                "chatrooms": json.dumps(
                    [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
                ),
                "username": request.user.username,
                "sound_data": json.dumps([]),  # Empty data on error
                "error_message": str(e),
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
