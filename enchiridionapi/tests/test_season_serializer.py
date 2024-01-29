from django.test import TestCase
from ..serializers import SeasonSerializer, SimpleSeasonSerializer

class SeasonSerializerTest(TestCase):
    """ Test module for season serializer """

    def setUp(self):
        self.tmdb_simple_season = {
            "id": 1,
            "air_date": "2000-01-01",
            "name": "test season 1 name",
            "overview": "test season 1 overview",
            "season_number": 1,
            "episode_count": 10,
            "poster_path": "test-season-still-path-1"
        }
        self.tmdb_season = {
            "id": 1,
            "air_date": "2000-01-01",
            "name": "test season 1 name",
            "overview": "test season 1 overview",
            "season_number": 1,
            "episodes": [],
            "poster_path": "test-season-still-path-1"
        }
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

    def test_simple_season_serializer(self):
        serializer = SimpleSeasonSerializer(self.tmdb_simple_season)

        data = serializer.data

        self.assertEqual(data['id'], self.tmdb_simple_season['id'])
        self.assertEqual(data['air_date'], self.tmdb_simple_season['air_date'])
        self.assertEqual(data['name'], self.tmdb_simple_season['name'])
        self.assertEqual(data['overview'], self.tmdb_simple_season['overview'])
        self.assertEqual(data['season_number'], self.tmdb_simple_season['season_number'])
        self.assertEqual(data['episode_count'], self.tmdb_simple_season['episode_count'])
        self.assertEqual(data['poster_path'], self.tmdb_simple_season['poster_path'])
        
    def test_season_serializer(self):
        serializer = SeasonSerializer(self.tmdb_season)

        data = serializer.data

        self.assertEqual(data['id'], self.tmdb_season['id'])
        self.assertEqual(data['air_date'], self.tmdb_season['air_date'])
        self.assertEqual(data['name'], self.tmdb_season['name'])
        self.assertEqual(data['overview'], self.tmdb_season['overview'])
        self.assertEqual(data['season_number'], self.tmdb_season['season_number'])
        self.assertEqual(len(data['episodes']), len(self.tmdb_season['episodes']))
        self.assertEqual(data['poster_path'], self.tmdb_season['poster_path'])