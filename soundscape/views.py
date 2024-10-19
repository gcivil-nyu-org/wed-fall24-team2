from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import SignupForm
from chatroom.models import Chatroom

import os
import json


def homepage(request):
    return render(
        request,
        "soundscape/homepage.html",
        {
            "mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN"),
            "chatrooms": json.dumps(
                [model_to_dict(chatroom) for chatroom in Chatroom.objects.all()]
            ),
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
