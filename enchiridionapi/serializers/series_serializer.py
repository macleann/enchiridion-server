from rest_framework import serializers
from .season_serializer import SimpleSeasonSerializer

class SeriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    backdrop_path = serializers.CharField(allow_blank=True, required=False)
    poster_path = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField()
    overview = serializers.CharField(allow_blank=True, required=False)
    seasons = SimpleSeasonSerializer(many=True)
