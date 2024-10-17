from django.shortcuts import render, redirect


from .forms import SignupForm
import os


def homepage(request):
    return render(
        request,
        "soundscape/homepage.html",
        {"mapbox_access_token": os.environ.get("MAPBOX_ACCESS_TOKEN")},
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
