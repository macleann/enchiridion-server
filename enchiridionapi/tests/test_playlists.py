from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Playlist

class PlaylistTest(TestCase):
    """ Test module for Playlist model """

    def setUp(self):
        user = User.objects.create_user(username='test_user', password='password')
        Playlist.objects.create(
            user=user,
            name='test playlist',
            description='this is a test playlist')

    def test_playlist(self):
        playlist=Playlist.objects.get(name='test playlist')
        self.assertEqual(playlist.user.username, 'test_user')
        self.assertEqual(playlist.name, 'test playlist')
        self.assertEqual(playlist.description, 'this is a test playlist')
