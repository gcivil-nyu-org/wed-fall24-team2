from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from soundscape_user.models import SoundFileUser
from soundscape_user.models import SoundDescriptor

from .forms import SignupForm
from chatroom.models import Chatroom

import requests

import os
import json

from better_profanity import profanity


def homepage(request):
    # Query SoundFileUser data
    user_sound_files = SoundFileUser.objects.all()
    user_sound_files_data = json.dumps(
        [model_to_dict(sound) for sound in user_sound_files]
    )

    sound_descriptors = SoundDescriptor.objects.all()
    sound_descriptors_data = json.dumps(
        [model_to_dict(sound) for sound in sound_descriptors]
    )

    return render(
        request,
        "soundscape/homepage.html",
        {
            "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
            "chatrooms": json.dumps(
                [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
            ),
            "username": request.user.username,
            "user_sound_data": user_sound_files_data,
            "sound_descriptors": sound_descriptors_data,
        },
    )


def get_noise_data(request):
    if request.method == "POST":
        conditions = json.loads(request.body)

        API_URL = "https://data.cityofnewyork.us/resource/hbc2-s6te.json"
        APP_TOKEN = os.environ.get("NYC_OPEN_DATA_APP_TOKEN")
        headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

        BATCH_SIZE = 1000
        TOTAL_ROWS = 1000
        all_data = []

        # Get filter parameters from the request (if any)
        sound_type = conditions["soundType"] or ["Noise"]
        date_from = conditions["dateFrom"]
        date_to = conditions["dateTo"]

        # Create where clause for sound types
        sound_type_conditions = " OR ".join(
            [f"starts_with(complaint_type, '{stype}')" for stype in sound_type]
        )
        where_clause = f"({sound_type_conditions})"

        # Apply date filters if provided
        if date_from:
            where_clause += f" AND created_date >= '{date_from}'"
        if date_to:
            where_clause += f" AND created_date <= '{date_to}'"

        try:
            batch_offsets = range(0, TOTAL_ROWS, BATCH_SIZE)

            for offset in batch_offsets:
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

            return JsonResponse({"sound_data": json.dumps(all_data)}, status=200)

        except Exception as e:
            return JsonResponse(
                {"error": f"Error fetching noise data: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


def check_profanity(request):
    if request.method == "POST":
        message = request.body.decode("utf-8")

        try:
            # The output is a Boolean value True or False
            value = profanity.contains_profanity(message)
            return JsonResponse({"value": str(int(value))}, status=200)
        except Exception:
            return JsonResponse({"value": str(1)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def filter_profanity(request):
    if request.method == "POST":
        message = request.body.decode("utf-8")

        try:
            censored_message = profanity.censor(message)
            return JsonResponse({"message": str(censored_message)}, status=200)
        except Exception:
            return JsonResponse({"message": str(message)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SignupForm()

    return render(request, "soundscape/signup.html", {"form": form})
