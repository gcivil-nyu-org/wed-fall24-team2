from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from soundscape_user.models import SoundFileUser
from soundscape_user.models import SoundDescriptor

from .forms import SignupForm
from chatroom.models import Chatroom
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

import requests


import os
import json

from better_profanity import profanity

from django.views import View
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.http import HttpResponseRedirect

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache


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


def fetch_batch(url: str, params: Dict, headers: Dict) -> List[Dict]:
    """Fetch a single batch of data"""
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching batch with offset {params.get('$offset')}: {str(e)}")
        return []


def get_noise_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        conditions = json.loads(request.body)

        # Generate a unique cache key based on the request conditions
        cache_key = f"noise_data_full_{json.dumps(conditions, sort_keys=True)}"

        # Try to get cached first
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"Retrieved data from cache for key: {cache_key}")

            # Ensure the response matches the original API response structure
            response_data = {
                "sound_data": cached_data.get("sound_data", []),
                "total_records": cached_data.get("total_records", 0),
                "records_requested": cached_data.get("records_requested", 0),
            }

            return JsonResponse(response_data, status=200, safe=False)

        # Constants
        API_URL = "https://data.cityofnewyork.us/resource/hbc2-s6te.json"
        APP_TOKEN = os.environ.get("NYC_OPEN_DATA_APP_TOKEN")
        headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}
        TOTAL_RECORDS = 5000
        BATCH_SIZE = 1000
        MAX_WORKERS = 5  # Number of concurrent requests

        # Build the where clause
        sound_type = conditions.get("soundType") or ["Noise"]
        sound_type_conditions = " OR ".join(
            [f"starts_with(complaint_type, '{stype}')" for stype in sound_type]
        )
        where_clause = f"({sound_type_conditions})"

        if date_from := conditions.get("dateFrom"):
            where_clause += f" AND created_date >= '{date_from}'"
        if date_to := conditions.get("dateTo"):
            where_clause += f" AND created_date <= '{date_to}'"

        # Prepare batch parameters for parallel requests
        batch_params = [
            {
                "$limit": BATCH_SIZE,
                "$offset": offset,
                "$where": where_clause,
                "$order": "created_date DESC",  # Consistent ordering
            }
            for offset in range(0, TOTAL_RECORDS, BATCH_SIZE)
        ]

        # Fetch data in parallel
        all_data = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all batch requests
            future_to_params = {
                executor.submit(fetch_batch, API_URL, params, headers): params
                for params in batch_params
            }

            # Process results as they complete
            for future in future_to_params:
                batch_data = future.result()
                if not batch_data:  # If we get an empty response, we've hit the end
                    break
                all_data.extend(batch_data)

        # Prepare response data
        response_data = {
            "sound_data": all_data,
            "total_records": len(all_data),
            "records_requested": TOTAL_RECORDS,
        }

        # Cache the entire response for 1 day
        cache.set(cache_key, response_data, timeout=86400)
        print(f"Cached data for key: {cache_key}")

        return JsonResponse(response_data, status=200, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": f"API request failed: {str(e)}"},
            status=503,  # Service Unavailable
        )
    except json.JSONDecodeError as e:
        return JsonResponse(
            {"error": f"Invalid JSON in request body - {str(e)}"},
            status=400,  # Bad Request
        )
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


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


class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            # Notify WebSocket consumers to disconnect
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}", {"type": "logout_message"}
            )

            Session.objects.filter(session_key=request.session.session_key).delete()
            logout(request)

        return HttpResponseRedirect(reverse("soundscape:homepage"))


def validate_session(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True})
    return JsonResponse({"authenticated": False}, status=401)
