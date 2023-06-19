import requests, os
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from enchiridionapi.serializers import SeriesSerializer

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

class SeriesView(ViewSet):
    """Series ViewSet

    Args:
        ViewSet: Inherits from the ViewSet class in the rest_framework package
    """

    def list (self, request):
        """GET a list of series from the TMDB API that match the search parameter

        Args:
            request (dict): the request object from the client

        Returns:
            a JSON serialized list of series from the TMDB API
        """
        search_parameter = request.query_params.get('q')

        if search_parameter is None:
            return Response({"message": "Please enter a search parameter."}, status=status.HTTP_400_BAD_REQUEST)

        url = f'https://api.themoviedb.org/3/search/tv?query={search_parameter}'

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"
        }

        tmdb_response = requests.get(url, headers=headers)

        if tmdb_response.status_code == status.HTTP_200_OK:
            json_tmdb_response = tmdb_response.json()
            serializer = SeriesSerializer(json_tmdb_response['results'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        """GET a specific series from the TMDB API

        Args:
            request (dict): the request object from the client
            pk (int): the primary key of the series

        Returns:
            a JSON serialized series from the TMDB API
        """
        url = f'https://api.themoviedb.org/3/tv/{pk}'

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"
        }

        tmdb_response = requests.get(url, headers=headers)

        if tmdb_response.status_code == status.HTTP_200_OK:
            json_tmdb_response = tmdb_response.json()
            serializer = SeriesSerializer(json_tmdb_response)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch data from TMDB API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
