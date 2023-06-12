from rest_framework import serializers
from .episode_serializer import EpisodeSerializer

class SeasonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    season_number = serializers.IntegerField()
    air_date = serializers.DateField(required=False)
    name = serializers.CharField(max_length=100)
    poster_path = serializers.CharField(max_length=255, allow_blank=True, required=False)
    overview = serializers.CharField(allow_blank=True, required=False)
    episodes = EpisodeSerializer(many=True)

class SimpleSeasonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    air_date = serializers.DateField(required=False)
    name = serializers.CharField()
    overview = serializers.CharField(allow_blank=True, required=False)
    season_number = serializers.IntegerField()
    episode_count = serializers.IntegerField()
    poster_path = serializers.CharField(allow_blank=True, required=False)
