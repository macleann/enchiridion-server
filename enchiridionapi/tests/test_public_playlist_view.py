from django.test import TestCase, Client
from django.urls import reverse
from enchiridionapi.models import Playlist, Like
from django.contrib.auth.models import User

class PlaylistViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # the point of this is to create multiple user objects we can use to like playlists
        users = {}
        for i in range(1, 4):
            username = f'test_user_{i}'
            users[username] = User.objects.create_user(username=username, password='password')
        # we'll then need to create a couple of playlist objects as well
        self.playlists = {}
        for i in range(1, 4):
            self.playlists[i] = Playlist.objects.create(
                user=users[f'test_user_{i}'],
                name=f'test playlist {i}',
                description=f'this is the description for test playlist {i}'
            )
        # lastly, we'll need to create a number of like objects
        # the amount of like objects will need to descend per playlist
        # for instance, let's say we have 3 playlists and 3 users
        # we'll need 3 likes on playlist 1, 2 likes on playlist 2, and 1 like on playlist 3
        for i in range(1, 4):
            for j in range(1, i + 1):
                Like.objects.create(
                    user=User.objects.get(username='test_user_{}'.format(j)),
                    playlist=self.playlists[i])

    def test_public_playlist_list_view(self):
        response = self.client.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test playlist 1')

    def test_public_playlist_trending_list_view(self):
        response = self.client.get(reverse('playlist-list'), QUERY_STRING='trending=true&days=7')
        self.assertEqual(response.status_code, 200)
        playlists = response.json()
        for playlist in playlists:
            self.assertGreater(playlist['likes_count'], 0)

    def test_public_playlist_trending_list_order_view(self):
        response = self.client.get(reverse('playlist-list'), QUERY_STRING='trending=true&days=7')
        self.assertEqual(response.status_code, 200)

        playlists = response.json()

        # check that the playlists are ordered correctly
        for i in range(len(playlists) - 1):
            self.assertGreaterEqual(playlists[i]['likes_count'], playlists[i + 1]['likes_count'])

    def test_public_playlist_retrieve_view(self):
        response = self.client.get(f'/playlists/{self.playlists[1].id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test playlist 1')