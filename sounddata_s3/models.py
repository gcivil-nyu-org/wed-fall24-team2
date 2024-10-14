from django.db import models

class NYCIncidentSoundData(models.Model):
    unique_key = models.CharField(max_length=100, primary_key=True)
    created_date = models.DateTimeField()
    closed_date = models.DateTimeField(null=True, blank=True)
    complaint_type = models.CharField(max_length=255)
    location_type = models.CharField(max_length=255, null=True, blank=True)
    incident_zip = models.CharField(max_length=10, null=True, blank=True)
    incident_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    resolution_description = models.TextField(null=True, blank=True)
    borough = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.complaint_type} - {self.unique_key}"


class NYCSoundFile(models.Model):
    unique_key = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    sound_file_url = models.URLField()

    
    