from django.contrib import admin
from enchiridionapi import models

admin.site.register(models.Playlist)
admin.site.register(models.PlaylistEpisode)
admin.site.register(models.Episode)
admin.site.register(models.Like)