# Generated by Django 4.1.1 on 2024-10-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("soundscape_user", "0002_rename_soundfile_soundfileuser"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="soundfileuser",
            name="user",
        ),
        migrations.AddField(
            model_name="soundfileuser",
            name="user_name",
            field=models.CharField(default="Anonymous", max_length=255),
        ),
    ]
