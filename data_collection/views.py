# data_collection/views.py
from django.shortcuts import render
from django.db.models import Count
from .models import NYCIncidentData


def borough_with_most_incidents(request):
    # Count the number of incidents per borough
    incidents_by_borough = (
        NYCIncidentData.objects.values("borough")
        .annotate(incident_count=Count("borough"))
        .order_by("-incident_count")
    )

    # Get the borough with the most incidents
    if incidents_by_borough:
        top_borough = incidents_by_borough[0]  # The borough with the highest count
    else:
        top_borough = None

    # Render the correct template without additional folder structure
    return render(request, "noisy-borough.html", {"top_borough": top_borough})
