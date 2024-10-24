from django.db import models
from django.contrib.auth.models import User

class SoundFileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sound_descriptor = models.CharField(max_length=255)
    s3_file_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.s3_file_name}'
