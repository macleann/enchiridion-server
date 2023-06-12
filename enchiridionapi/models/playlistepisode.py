"""Module defining the playlist model"""
from django.db import models

class PlaylistEpisode(models.Model):

    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)
    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE)
    order_number = models.IntegerField()
