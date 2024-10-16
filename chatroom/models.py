from django.db import models


class Explorer(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)


class Chatroom(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_length=400)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    explorer = models.ForeignKey(
        Explorer, null=True, blank=True, on_delete=models.SET_NULL
    )
