import random
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from enchiridionapi.models import Playlist, PlaylistEpisode

class UserPlaylistViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.unauthorized_client = APIClient()
        self.playlists = {}
        for i in range(1, 4):
            self.playlists[i] = Playlist.objects.create(
                user=self.user,
                name=f'test playlist {i}',
                description=f'this is the description for test playlist {i}'
            )

        # Helper function to DRY up some code:
        def generate_random_episode_data():
            return {
                'id': random.randint(1, 100),
                'series_id': 1,
                'series_name': 'test episode 1 series name',
                'season_number': 1,
                'episode_number': 1,
                'order_number': 1,
                'name': 'test episode 1 name',
                'overview': 'test episode 1 overview',
                'air_date': '2000-01-01',
                'runtime': 28,
                'still_path': '/test-episode-1-still-path'
            }
        self.create_data = {
            'name': 'New Playlist',
            'description': 'This is a new playlist',
            'episodes': [generate_random_episode_data()]
        }
        self.update_data = {
            'name': 'Updated Playlist',
            'description': 'This playlist has been updated',
            'episodes': [generate_random_episode_data()]
        }

    def test_user_playlist_list_view(self):
        response = self.client.get(reverse('user-playlist-list'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_user_playlist_create_view(self):
        response = self.client.post(reverse('user-playlist-list'), self.create_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response_data, dict)

        # Fetch the newly created playlist and check its episodes through PlaylistEpisode
        new_playlist = Playlist.objects.get(id=response_data['id'])
        self.assertEqual(new_playlist.episodes.count(), len(self.create_data['episodes']))

        # Check that the associated episode exists
        episode_id = self.create_data['episodes'][0]['id']
        self.assertTrue(new_playlist.episodes.filter(tmdb_id=episode_id).exists())

    def test_user_playlist_update_view(self):
        playlist_id = self.playlists[1].id
        # Make some assertions about the playlist before we update it
        self.assertEqual(self.playlists[1].name, 'test playlist 1')
        self.assertEqual(self.playlists[1].episodes.count(), 0)

        # Then pass the update_data
        response = self.client.put(reverse('user-playlist-detail', kwargs={'pk': playlist_id}), self.update_data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, dict)

        # Fetch the updated data and make sure it was updated
        updated_playlist = Playlist.objects.get(id=response_data['id'])
        self.assertEqual(updated_playlist.name, self.update_data['name'])
        self.assertEqual(updated_playlist.episodes.count(), len(self.update_data['episodes']))

        # Check that the associated episode has been updated
        updated_episode_id = self.update_data['episodes'][0]['id']
        self.assertTrue(updated_playlist.episodes.filter(tmdb_id=updated_episode_id).exists())

    def test_user_playlist_destroy_view(self):
        playlist_id = self.playlists[1].id

        response = self.client.delete(reverse('user-playlist-detail', kwargs={'pk': playlist_id}), format='json')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Playlist.DoesNotExist):
            Playlist.objects.get(id=playlist_id)
        self.assertEqual(PlaylistEpisode.objects.filter(playlist_id=playlist_id).count(), 0)

    def test_get_without_authentication(self):
        response = self.unauthorized_client.get(reverse('user-playlist-list'))
        self.assertEqual(response.status_code, 403)

    def test_post_without_authentication(self):
        response = self.unauthorized_client.post(reverse('user-playlist-list'), self.create_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_put_without_authentication(self):
        playlist_id = self.playlists[1].id
        response = self.unauthorized_client.put(reverse('user-playlist-detail', kwargs={'pk': playlist_id}), self.update_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_delete_without_authentication(self):
        playlist_id = self.playlists[1].id
        response = self.unauthorized_client.delete(reverse('user-playlist-detail', kwargs={'pk': playlist_id}), format='json')
        self.assertEqual(response.status_code, 403)