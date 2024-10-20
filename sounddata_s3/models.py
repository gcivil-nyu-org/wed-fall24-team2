from django.db import models


class NYCSoundFile(models.Model):
    unique_key = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    sound_file_url = models.URLField()
