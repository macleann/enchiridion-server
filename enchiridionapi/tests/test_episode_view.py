import os
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from enchiridionapi.models import Episode

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

class EpisodeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.episode = Episode.objects.create(
            tmdb_id=1,
            series_id=1,
            series_name='test series name 1',
            season_number=1,
            episode_number=1,
            name='test episode name 1',
            air_date='2000-01-01',
            overview='test episode overview 1',
            runtime=25,
            still_path='/test-episode-still-path-1'
        )

    def test_list_view(self):
        response = self.client.get(reverse('episode-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test episode name 1')

    def test_retrieve_view(self):
        response = self.client.get(reverse('episode-detail', args=[self.episode.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test episode name 1')

    @patch('requests.get')
    def test_tmdb_list_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { "episodes": [] }

        for i in range(1, 4):
            episode_dict = {
                "id": i,
                "tmdb_id": self.episode.tmdb_id,
                "series_id": self.episode.series_id,
                "series_name": 'test series name 1',
                "season_number": self.episode.season_number,
                "episode_number": i,
                "name": 'test episode name {}'.format(i),
                "air_date": '2000-01-{:02d}'.format(i),
                "overview": 'test episode overview {}'.format(i),
                "runtime": 25,
                "still_path": '/test-episode-still-path-{}'.format(i)
            }
            mock_get.return_value.json.return_value['episodes'].append(episode_dict)
        
        response = Client().get('/episodes/tmdb_episodes', QUERY_STRING=f'series_id={self.episode.tmdb_id}&season_number={self.episode.season_number}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertIsInstance(response.json()[0], dict)

    @patch('requests.get')
    def test_tmdb_retrieve_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "tmdb_id": 1,
            "series_id": 1,
            "series_name": 'test series name 1',
            "season_number": 1,
            "episode_number": 1,
            "name": 'test episode name 1',
            "air_date": '2000-01-01',
            "overview": 'test episode overview 1',
            "runtime": 25,
            "still_path": '/test-episode-still-path-1'
        }

        response = Client().get('/episodes/tmdb_single_episode', QUERY_STRING='series_id=1&season_number=1&episode_number=1')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
