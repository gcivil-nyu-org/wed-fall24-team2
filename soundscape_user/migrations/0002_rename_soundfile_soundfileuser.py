# Generated by Django 4.1.1 on 2024-10-24 23:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("soundscape_user", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SoundFile",
            new_name="SoundFileUser",
        ),
    ]
