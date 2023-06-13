import os
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from enchiridionapi.models import Playlist
from enchiridionapi.serializers import PlaylistSerializer

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

class PublicPlaylistView(ViewSet):
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Gets a list of playlists"""
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handles GET requests for single playlist"""
        try:
            playlist = Playlist.objects.get(pk=pk)
            serializer = PlaylistSerializer(playlist, context={'request': request})
            return Response(serializer.data)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
