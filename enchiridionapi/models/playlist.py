"""Module defining the playlist model"""
from django.db import models
from django.contrib.auth.models import User

class Playlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    episodes = models.ManyToManyField("Episode", through="PlaylistEpisode", related_name="playlists")
