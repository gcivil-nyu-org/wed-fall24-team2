# Generated by Django 4.1.1 on 2024-10-07 01:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NYCIncidentData",
            fields=[
                (
                    "unique_key",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("created_date", models.DateTimeField()),
                ("closed_date", models.DateTimeField(blank=True, null=True)),
                ("complaint_type", models.CharField(max_length=255)),
                (
                    "location_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "incident_zip",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "incident_address",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(max_length=100)),
                ("status", models.CharField(max_length=100)),
                ("resolution_description", models.TextField(blank=True, null=True)),
                ("borough", models.CharField(max_length=100)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
