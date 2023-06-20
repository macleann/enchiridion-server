from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from enchiridionapi.serializers import EpisodeSerializer, LocalEpisodeSerializer
from enchiridionapi.models import Episode
import requests, os

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

class EpisodeView(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        """
        Gets a list of episodes from the local database

        Returns: a JSON serialized list of episodes from the local database
        """
        episodes = Episode.objects.all()
        serializer = LocalEpisodeSerializer(episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieves an episode from the local database by primary key

        Returns: a JSON serialized episode from the local database
        """
        try:
            episode = Episode.objects.get(pk=pk)
            serializer = LocalEpisodeSerializer(episode)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Episode.DoesNotExist:
            return Response({"error": "Episode not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def tmdb_episodes(self, request):
        """
        Gets a list of episodes from the TMDB API

        Requires: season_number = the season number

        Returns: a JSON serialized list of episodes from the TMDB API
        """
        series_id = request.query_params.get('series_id')
        season_number = request.query_params.get('season_number')
        
        if series_id is None or season_number is None:
            return Response({"error": "Series id and season number are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f'https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}'
        headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {TMDB_API_KEY}"
                }
        
        tmdb_response = requests.get(url, headers=headers)

        if tmdb_response.status_code == 200:
            json_tmdb_response = tmdb_response.json()
            serializer = EpisodeSerializer(json_tmdb_response['episodes'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def tmdb_single_episode(self, request):
        """
        Gets an episode from the TMDB API

        Requires:
            season_number = the season number
            episode_number = the episode number

        Returns: a JSON serialized episode from the TMDB API
        """
        series_id = request.query_params.get('series_id')
        season_number = request.query_params.get('season_number')
        episode_number = request.query_params.get('episode_number')
        
        if series_id is None or season_number is None or episode_number is None:
            return Response({"error": "Series id and season and episode numbers are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f'https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}/episode/{episode_number}'
        headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {TMDB_API_KEY}"
                }
        
        tmdb_response = requests.get(url, headers=headers)

        if tmdb_response.status_code == 200:
            episode = tmdb_response.json()
            serializer = EpisodeSerializer(episode)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
