from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from enchiridionapi.models import Like, Playlist

class LikeView(ViewSet):
    """
    A viewset for handling likes on playlists.

    create:
    Creates a new like for a playlist.

    destroy:
    Deletes an existing like for a playlist.
    """
    
    def create(self, request):
        playlist = Playlist.objects.get(pk=request.data.get('playlist_id'))
        like = Like.objects.create(user=request.user, playlist=playlist)
        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
            like = Like.objects.get(user=request.user, playlist=playlist)
            if like.user_id != request.user.id:
                return Response({"message": "You can only delete your own likes."}, status=status.HTTP_403_FORBIDDEN)
            like.delete()
            return Response({'message': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'message': 'Like does not exist'}, status=status.HTTP_404_NOT_FOUND)