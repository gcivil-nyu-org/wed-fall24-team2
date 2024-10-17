from django.urls import path

from . import views

app_name = "chatroom"
urlpatterns = [
    path("", views.chatroom, name="chatroom"),
]
