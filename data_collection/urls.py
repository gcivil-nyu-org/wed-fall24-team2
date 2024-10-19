from django.urls import path
from . import views

urlpatterns = [
    path("top-borough/", views.borough_with_most_incidents, name="top_borough"),
]
