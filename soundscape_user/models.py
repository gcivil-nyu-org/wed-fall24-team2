from django.db import models


class SoundFileUser(models.Model):
    user_name = models.CharField(max_length=255, default="Anonymous")
    sound_descriptor = models.CharField(max_length=255)
    s3_file_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.s3_file_name}"
