"""Module defining the like model"""
from django.db import models
from django.contrib.auth.models import User
from .playlist import Playlist

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now_add=True)
