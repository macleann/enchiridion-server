from django.test import TestCase
from django.contrib.auth.models import User
from dateutil.parser import parse
from ..models import Like, Playlist
from ..serializers import LikeSerializer

class LikeSerializerTest(TestCase):
    """ Test module for like serializer """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='test playlist',
            description='this is a test playlist')
        self.like = Like.objects.create(
            user=self.user,
            playlist=self.playlist
        )

    def test_like_serializer(self):
        serializer = LikeSerializer(self.like)

        data = serializer.data

        self.assertEqual(data['id'], self.like.id)
        self.assertEqual(data['user'], self.like.user.id)
        self.assertEqual(data['playlist'], self.like.playlist.id)
        self.assertEqual(parse(data['date_liked']), self.like.date_liked)
