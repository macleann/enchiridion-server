from rest_framework import serializers
from enchiridionapi.models import Episode

class EpisodeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    air_date = serializers.DateField()
    season_number = serializers.IntegerField()
    episode_number = serializers.IntegerField()
    overview = serializers.CharField(allow_blank=True, required=False)
    runtime = serializers.IntegerField()
    still_path = serializers.CharField(max_length=255, allow_blank=True, required=False)

class LocalEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'name', 'season_number', 'episode_number',
                  'air_date', 'overview', 'runtime', 'still_path']
