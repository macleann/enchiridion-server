import requests, os
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from enchiridionapi.serializers import SeasonSerializer, SimpleSeasonSerializer

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

class SeasonView(ViewSet):
    def list(self, request):
        """
        Gets a list of seasons from the TMDB API

        Returns: a JSON serialized list of seasons from the TMDB API
        """
        # Set the url to query the API
        url = f'https://api.themoviedb.org/3/tv/15260'

        # Set the appropriate headers according to the documentation at
        # https://developer.themoviedb.org/reference/intro/getting-started
        headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {TMDB_API_KEY}"
                }
        
        # Get from the API
        tmdb_response = requests.get(url, headers=headers)

        # If the request is successful
        if tmdb_response.status_code == 200:
            # Parse the list into JSON
            json_tmdb_response = tmdb_response.json()
            # And pass that JSON list through the serializer
            serializer = SimpleSeasonSerializer(json_tmdb_response['seasons'], many=True)
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the request was not successful, return an error
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        """
        Gets a specific season from the TMDB API

        Requires: pk = the season number

        Returns: a JSON serialized season from the TMDB API
        """
        # Set the url to query the API
        url = f'https://api.themoviedb.org/3/tv/15260/season/{pk}'

        # Set the appropriate headers according to the documentation at
        # https://developer.themoviedb.org/reference/intro/getting-started
        headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {TMDB_API_KEY}"
                }
        
        # Get from the API
        tmdb_response = requests.get(url, headers=headers)

        # If the request is successful
        if tmdb_response.status_code == 200:
            # Parse the list into JSON
            season = tmdb_response.json()
            # And pass that JSON list through the serializer
            serializer = SeasonSerializer(season)
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the request was not successful, return an error
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)