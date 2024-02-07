from django.test import TestCase
from ..serializers import SeriesSerializer

class SeriesSerializerTest(TestCase):
    """ Test module for series serializer """

    def setUp(self):
        self.tmdb_series_response = {
            "id": 1,
            "backdrop_path": "test-series-backdrop-path-1",
            "poster_path": "test-series-poster-path-1",
            "name": "test series name 1",
            "overview": "test series overview 1",
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
            "first_air_date": "2000-01-01"
        }

    def test_series_serializer(self):
        serializer = SeriesSerializer(self.tmdb_series_response)

        data = serializer.data

        self.assertEqual(data["id"], self.tmdb_series_response["id"])
        self.assertEqual(data["backdrop_path"], self.tmdb_series_response["backdrop_path"])
        self.assertEqual(data["poster_path"], self.tmdb_series_response["poster_path"])
        self.assertEqual(data["name"], self.tmdb_series_response["name"])
        self.assertEqual(data["overview"], self.tmdb_series_response["overview"])
        self.assertEqual(data["seasons"], self.tmdb_series_response["seasons"])
        self.assertEqual(data["first_air_date"], self.tmdb_series_response["first_air_date"])
