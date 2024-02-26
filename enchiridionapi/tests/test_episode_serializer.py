from django.test import TestCase
from ..models import Episode
from ..serializers import LocalEpisodeSerializer, EpisodeSerializer

class EpisodeSerializerTest(TestCase):
    """ Test module for episode serializer """

    def setUp(self):
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

    def test_local_episode_serializer(self):
        serializer = LocalEpisodeSerializer(self.episode)

        data = serializer.data

        self.assertEqual(data['id'], self.episode.id)
        self.assertEqual(data['tmdb_id'], self.episode.tmdb_id)
        self.assertEqual(data['series_id'], self.episode.series_id)
        self.assertEqual(data['series_name'], self.episode.series_name)
        self.assertEqual(data['name'], self.episode.name)
        self.assertEqual(data['season_number'], self.episode.season_number)
        self.assertEqual(data['episode_number'], self.episode.episode_number)
        self.assertEqual(data['air_date'], str(self.episode.air_date))
        self.assertEqual(data['overview'], self.episode.overview)
        self.assertEqual(data['runtime'], self.episode.runtime)
        self.assertEqual(data['still_path'], self.episode.still_path)

    def test_episode_serializer(self):
        serializer = EpisodeSerializer(self.episode)

        data = serializer.data

        self.assertEqual(data['id'], self.episode.id)
        self.assertEqual(data['name'], self.episode.name)
        self.assertEqual(data['season_number'], self.episode.season_number)
        self.assertEqual(data['episode_number'], self.episode.episode_number)
        self.assertEqual(data['air_date'], str(self.episode.air_date))
        self.assertEqual(data['overview'], self.episode.overview)
        self.assertEqual(data['runtime'], self.episode.runtime)
        self.assertEqual(data['still_path'], self.episode.still_path)