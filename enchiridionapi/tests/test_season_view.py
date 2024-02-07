from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class SeasonViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tmdb_simple_season = []
        for i in range(1, 4):
            season_dict = {
                "id": i,
                "air_date": "2000-01-{:02d}".format(i),
                "name": "test season {} name".format(i),
                "overview": "test season {} overview".format(i),
                "season_number": i,
                "episode_count": i*10,
                "poster_path": "test-season-still-path-{}".format(i)
            }
            self.tmdb_simple_season.append(season_dict)
        self.tmdb_season = self.tmdb_simple_season[0].copy()
        self.tmdb_season.pop("episode_count")
        self.tmdb_season["episodes"] = []
        for i in range(1, 4):
            episode_dict = {
                "id": i,
                "tmdb_id": i,
                "series_id": 1,
                "series_name": 'test series name 1',
                "season_number": 1,
                "episode_number": i,
                "name": 'test episode name {}'.format(i),
                "air_date": '2000-01-{:02d}'.format(i),
                "overview": 'test episode overview {}'.format(i),
                "runtime": 25,
                "still_path": '/test-episode-still-path-{}'.format(i)
            }
            self.tmdb_season['episodes'].append(episode_dict)

    @patch('requests.get')
    def test_season_list_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"seasons": self.tmdb_simple_season}

        response = self.client.get(reverse('season-list'), QUERY_STRING='series_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertIsInstance(response.json()[0], dict)

    @patch('requests.get')
    def test_season_retrieve_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.tmdb_season

        response = self.client.get(f"/seasons/{self.tmdb_season['season_number']}", QUERY_STRING='series_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)