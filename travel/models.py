from django.contrib.auth.models import User
from django.db import models


class Destination(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    travel_category = models.CharField(max_length=100, blank=True)
    attractions = models.TextField(blank=True)
    best_season = models.CharField(max_length=100, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="destinations/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinations")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
