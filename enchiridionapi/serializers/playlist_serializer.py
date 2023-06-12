from rest_framework import serializers
from enchiridionapi.models import Playlist

class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = ('id', 'user', 'name', 'description', 'episodes')
        depth = 1
