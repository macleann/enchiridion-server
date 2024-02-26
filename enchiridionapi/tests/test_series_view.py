from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class SeriesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tmdb_search_results = []
        for i in range(1, 4):
            series_dict = {
                "id": i,
                "backdrop_path": "test-series-backdrop-path-{}".format(i),
                "poster_path": "test-series-poster-path-{}".format(i),
                "name": "test series name {}".format(i),
                "overview": "test series overview {}".format(i),
                "seasons": [
                    {
                    "id": 1,
                    "air_date": "2000-01-01",
                    "name": "test season 1 name",
                    "overview": "test season 1 overview",
                    "season_number": 1,
                    "episode_count": 10,
                    "poster_path": "test-season-still-path-1"
                    }
                ],
                "first_air_date": "2000-01-{:02d}".format(i)
            }
            self.tmdb_search_results.append(series_dict)
        self.tmdb_single_series = self.tmdb_search_results[0].copy()

    @patch('requests.get')
    def test_series_list_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": self.tmdb_search_results}

        response = self.client.get(reverse('series-list'), QUERY_STRING='q=test series name')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertIsInstance(response.json()[0], dict)

    @patch('requests.get')
    def test_series_retrieve_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.tmdb_single_series

        response = self.client.get(reverse('series-detail', kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)