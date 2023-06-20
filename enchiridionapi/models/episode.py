"""Module defining the episode model"""
from django.db import models

class Episode(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    series_id = models.IntegerField()
    series_name = models.CharField(max_length=100)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    name = models.CharField(max_length=100)
    air_date = models.DateField()
    overview = models.TextField(blank=True, null=True)
    runtime = models.IntegerField()
    still_path = models.CharField(max_length=255, blank=True, null=True)
