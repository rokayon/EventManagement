from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    asset= models.ImageField(upload_to='event_asset/',blank=True,null=True)
                            #  ,default="media\event_asset\t-2.jpeg")
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    participants = models.ManyToManyField(User, related_name="rsvp_events", blank=True)

    def __str__(self):
        return self.name




