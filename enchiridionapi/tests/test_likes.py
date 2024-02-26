from django.test import TestCase
import datetime
from django.contrib.auth.models import User
from ..models import Playlist, Like

class LikeTest(TestCase):
    """ Test module for Like model """

    def setUp(self):
        user = User.objects.create_user(username='test_user', password='password')
        playlist = Playlist.objects.create(
            user=user,
            name='test playlist',
            description='this is a test playlist')
        Like.objects.create(
            user=user,
            playlist=playlist
        )
        self.user=user
        self.playlist=playlist

    def test_like(self):
        like=Like.objects.get(user=self.user, playlist=self.playlist)
        self.assertEqual(like.user.username, 'test_user')
        self.assertEqual(like.playlist.name, 'test playlist')
        self.assertIsInstance(like.date_liked, datetime.datetime)