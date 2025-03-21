# Generated by Django 5.1.6 on 2025-03-19 19:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="asset",
            field=models.ImageField(blank=True, null=True, upload_to="event_asset/"),
        ),
        migrations.AddField(
            model_name="event",
            name="participants",
            field=models.ManyToManyField(
                blank=True, related_name="rsvp_events", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="event",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name="Participant",
        ),
    ]
