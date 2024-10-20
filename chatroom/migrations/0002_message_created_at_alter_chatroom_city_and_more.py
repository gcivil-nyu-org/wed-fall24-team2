# Generated by Django 4.1.1 on 2024-10-20 18:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("chatroom", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="latitude",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="longitude",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]