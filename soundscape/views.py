from django.shortcuts import render
import os


def homepage(request):
    return render(
        request,
        "homepage.html",
        {"mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN")},
    )
