from django.db import models
from django.contrib.auth.models import AbstractUser


class Explorer(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=150, unique=True, default='default_username')  # Set default username

    def __str__(self):
        return self.username
    REQUIRED_FIELDS = ['email']


class Chatroom(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_length=400)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    explorer = models.ForeignKey(
        Explorer, null=True, blank=True, on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(auto_now_add=True)
