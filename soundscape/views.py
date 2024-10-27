from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import SignupForm
from chatroom.models import Chatroom
from django.http import JsonResponse


import requests

import os
import json


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
                "$where": "starts_with(complaint_type, 'Noise')",
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


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/login/")
    else:
        form = SignupForm()

    return render(request, "soundscape/signup.html", {"form": form})


def filtered_sound_data(request):
    API_URL = "https://data.cityofnewyork.us/resource/hbc2-s6te.json"
    APP_TOKEN = os.environ.get("NYC_OPEN_DATA_APP_TOKEN")
    headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

    BATCH_SIZE = 1000
    TOTAL_ROWS = 2000
    all_data = []

    # Get filter parameters from the request
    sound_type = request.GET.get("soundType", "Noise")
    date_from = request.GET.get("dateFrom")
    date_to = request.GET.get("dateTo")

    try:
        batch_offsets = range(0, TOTAL_ROWS, BATCH_SIZE)

        for offset in batch_offsets:
            # Initialize where clause
            where_clause = f"starts_with(complaint_type, '{sound_type}')"

            # Add date filters to the where clause if provided
            if date_from:
                where_clause += f" AND created_date >= '{date_from}'"
            if date_to:
                where_clause += f" AND created_date <= '{date_to}'"

            params = {
                "$limit": min(BATCH_SIZE, TOTAL_ROWS - offset),
                "$offset": offset,
                "$where": where_clause,
            }

            # Call the API with the constructed parameters
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()
            batch_data = response.json()

            if not batch_data:
                break

            all_data.extend(batch_data)
            if len(batch_data) < params["$limit"]:
                break

        # Render homepage.html instead of a separate template
        return render(
            request,
            "soundscape/homepage.html",
            {
                "sound_data": json.dumps(all_data),  # Pass filtered sound data
                "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
                "username": request.user.username,
                "chatrooms": json.dumps(
                    [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
                ),  # Include any other context needed
            },
        )

    except requests.RequestException as e:
        print(f"Error fetching filtered data: {str(e)}")
        return render(
            request,
            "soundscape/homepage.html",
            {
                "sound_data": json.dumps([]),  # Pass empty data on error
                "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
                "username": request.user.username,
                "chatrooms": json.dumps([]),  # Include any other context needed
                "error_message": str(e),  # Optional: Include error message if needed
            },
        )
