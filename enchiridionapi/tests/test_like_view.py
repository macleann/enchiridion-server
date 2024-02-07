from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Playlist

class LikeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test_user", password="password")
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='test playlist',
            description='this is a test playlist')

    def test_create_view(self):
        self.client.post('/login', {'username': 'test_user', 'password': 'password'})
        response = self.client.post('/likes', data={'playlist_id': self.playlist.id})
        self.assertEqual(response.status_code, 201)

    def test_destroy_view(self):
        self.client.post('/login', {'username': 'test_user', 'password': 'password'})
        self.client.post('/likes', data={'playlist_id': self.playlist.id})
        response = self.client.delete(f'/likes/{self.playlist.id}')
        self.assertEqual(response.status_code, 204)