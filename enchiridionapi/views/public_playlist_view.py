import os
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from enchiridionapi.models import Playlist
from enchiridionapi.serializers import PlaylistSerializer

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

class PublicPlaylistView(ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Gets a list of playlists"""
        if request.query_params.get('trending'):
            days_to_int = int(request.query_params.get('days'))
            trending_time = timezone.now() - timedelta(days=days_to_int)

            trending_playlists = PlaylistSerializer.setup_eager_loading(
                Playlist.objects
                .filter(like__date_liked__gte=trending_time)
                .annotate(likes_count=Count('like'))
                .order_by('-likes_count')
            )
            serializer = PlaylistSerializer(trending_playlists, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        playlists = PlaylistSerializer.setup_eager_loading(Playlist.objects.annotate(likes_count=Count('like')))
        serializer = PlaylistSerializer(playlists, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handles GET requests for single playlist"""
        try:
            playlist = PlaylistSerializer.setup_eager_loading(Playlist.objects.filter(pk=pk)).get()
            serializer = PlaylistSerializer(playlist, context={'request': request})
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
