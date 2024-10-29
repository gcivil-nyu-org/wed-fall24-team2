from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from soundscape_user.models import SoundFileUser 

from .forms import SignupForm
from chatroom.models import Chatroom


import requests

import os
import json


def homepage(request):
    API_URL = "https://data.cityofnewyork.us/resource/hbc2-s6te.json"
    APP_TOKEN = os.environ.get("NYC_OPEN_DATA_APP_TOKEN")
    headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

    BATCH_SIZE = 1000
    TOTAL_ROWS = 2000
    all_data = []

    # Get filter parameters from the request (if any)
    sound_type = request.GET.get("soundType", "Noise")
    date_from = request.GET.get("dateFrom")
    date_to = request.GET.get("dateTo")

    # Query SoundFileUser data
    user_sound_files = SoundFileUser.objects.all()
    user_sound_files_data = json.dumps([model_to_dict(sound) for sound in user_sound_files])

    try:
        batch_offsets = range(0, TOTAL_ROWS, BATCH_SIZE)

        for offset in batch_offsets:
            # Set the base where clause depending on whether a filter is applied
            where_clause = (
                f"starts_with(complaint_type, '{sound_type}')"
                if sound_type
                else "starts_with(complaint_type, 'Noise')"
            )

            # Apply date filters if provided
            if date_from:
                where_clause += f" AND created_date >= '{date_from}'"
            if date_to:
                where_clause += f" AND created_date <= '{date_to}'"

            params = {
                "$limit": min(BATCH_SIZE, TOTAL_ROWS - offset),
                "$offset": offset,
                "$where": where_clause,
            }

            # Fetch data from the API
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()

            batch_data = response.json()
            if not batch_data:
                break

            all_data.extend(batch_data)
            if len(batch_data) < params["$limit"]:
                break

        # Render homepage.html with the data (filtered or default)
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
                "user_sound_data": user_sound_files_data,
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
                "user_sounds": user_sound_files_data,
            },
        )


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SignupForm()

    return render(request, "soundscape/signup.html", {"form": form})
