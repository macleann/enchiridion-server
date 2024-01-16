import requests, os
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from enchiridionapi.models import Playlist, Episode, PlaylistEpisode
from enchiridionapi.serializers import PlaylistSerializer, LocalEpisodeSerializer

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

class UserPlaylistView(ViewSet):

    def list(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "You need to be logged in to view your playlists."},
                            status=status.HTTP_403_FORBIDDEN)
        
        playlists = Playlist.objects.filter(user_id=request.user.id)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        name = request.data.get('name')
        description = request.data.get('description')
        episodes = request.data.get('episodes')

        playlist = Playlist.objects.create(user=user, name=name, description=description)

        for episode_data in episodes:
            series_id = episode_data.get('series_id')
            season_number = episode_data.get('season_number')
            episode_number = episode_data.get('episode_number')
            order_number = episode_data.get('order_number')
            tmdb_id = episode_data.get('id')

            try:
                episode = Episode.objects.get(series_id=series_id, season_number=season_number, episode_number=episode_number)
            except Episode.DoesNotExist:
                episode_data['tmdb_id'] = tmdb_id
                serializer = LocalEpisodeSerializer(data=episode_data)
                if serializer.is_valid():
                    episode = serializer.save()
                else:
                    continue

            PlaylistEpisode.objects.create(playlist=playlist, episode=episode, order_number=order_number)

        playlist_serializer = PlaylistSerializer(playlist)

        return Response(playlist_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handles PUT requests for a playlist"""
        try:
            playlist = Playlist.objects.get(pk=pk)
            if playlist.user_id != request.user.id:
                return Response({"message": "You can only update your own playlists."}, status=status.HTTP_403_FORBIDDEN)
            # Get the new data from the request
            new_name = request.data.get('name')
            new_description = request.data.get('description')
            new_episodes = request.data.get('episodes')

            # Update the name and description
            playlist.name = new_name
            playlist.description = new_description

            # Remove existing episodes from the playlist
            PlaylistEpisode.objects.filter(playlist=playlist).delete()

            # Add the new episodes to the playlist
            for episode_data in new_episodes:
                series_id = episode_data.get('series_id')
                season_number = episode_data.get('season_number')
                episode_number = episode_data.get('episode_number')
                order_number = episode_data.get('order_number')
                tmdb_id = episode_data.get('id')

                # Same logic for fetching/creating the episode as in the create method...
                try:
                    # Check if episode exists in local DB
                    episode = Episode.objects.get(series_id=series_id, season_number=season_number, episode_number=episode_number)
                except Episode.DoesNotExist:
                    # If not, create it
                    # Add the TMDB ID to the episode data since creating a local episode generates a new, auto-incremented ID
                    episode_data['tmdb_id'] = tmdb_id
                    # Serialize the episode data to create the episode
                    serializer = LocalEpisodeSerializer(data=episode_data)
                    # Validate the data
                    if serializer.is_valid():
                        # Save the episode
                        episode = serializer.save()
                    else:
                        # If the data is invalid, skip this episode
                        continue

                # Now that we have the episode, add it to the playlist
                PlaylistEpisode.objects.create(playlist=playlist, episode=episode, order_number=order_number)

            playlist.save()

            # Serialize the playlist data to return it
            serializer = PlaylistSerializer(playlist)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        """Handles DELETE requests for a single playlist"""
        try:
            playlist = Playlist.objects.get(pk=pk)
            if playlist.user_id != request.user.id:
                return Response({"message": "You can only delete your own playlists."}, status=status.HTTP_403_FORBIDDEN)
            playlist.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
