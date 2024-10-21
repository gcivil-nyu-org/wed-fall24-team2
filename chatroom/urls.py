# chatroom/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL pattern that captures the room name
    path("<str:chatroom_name>/", views.chatroom, name="chatroom"),
]
