from rest_framework import serializers
from enchiridionapi.models import Playlist, PlaylistEpisode
from enchiridionapi.serializers import LocalEpisodeSerializer

class PlaylistSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'user_id', 'name', 'description', 'episodes']

    def get_episodes(self, obj):
        episodes = PlaylistEpisode.objects.filter(playlist=obj).order_by('order_number')
        episode_list = []
        for ep in episodes:
            episode_dict = LocalEpisodeSerializer(ep.episode).data
            episode_dict['order_number'] = ep.order_number
            episode_list.append(episode_dict)
        return episode_list
