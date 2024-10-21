from django.db import models
from django.contrib.auth.models import AbstractUser

class Explorer(AbstractUser):

    # Add related_name attributes to avoid the clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='explorer_set',  # Change related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='explorer_set',  # Change related_name to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.username
