from rest_framework import serializers
from django.db.models import Prefetch
from enchiridionapi.models import Playlist, PlaylistEpisode
from enchiridionapi.serializers import LocalEpisodeSerializer

class PlaylistSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'user_id', 'name', 'description', 'episodes', 'likes_count', 'is_liked']

    def get_episodes(self, obj):
        episode_playlist = obj.playlist_episodes
        serializer = LocalEpisodeSerializer([ep.episode for ep in episode_playlist], many=True)
        return serializer.data
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.like_set.filter(user=user).exists()
        return False

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
            Prefetch(
                'playlistepisode_set',
                queryset=PlaylistEpisode.objects.select_related('episode').order_by('order_number'),
                to_attr='playlist_episodes'
            )
        )
        return queryset
