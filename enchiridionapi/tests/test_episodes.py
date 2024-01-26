from django.test import TestCase
from ..models import Episode
import datetime

class EpisodeTest(TestCase):
    """ Test module for Episode model """

    def setUp(self):
        Episode.objects.create(
            tmdb_id=1,
            series_id=1,
            series_name='test series name 1',
            season_number=1,
            episode_number=1,
            name='test episode name 1',
            air_date='2000-01-01',
            overview='test episode overview 1',
            runtime=25,
            still_path='/test-episode-still-path-1')

    def test_episode(self):
        date_to_test = datetime.date(2000, 1, 1)
        episode=Episode.objects.get(name='test episode name 1')
        self.assertEqual(episode.tmdb_id, 1)
        self.assertEqual(episode.series_id, 1)
        self.assertEqual(episode.series_name, 'test series name 1')
        self.assertEqual(episode.season_number, 1)
        self.assertEqual(episode.episode_number, 1)
        self.assertEqual(episode.name, 'test episode name 1')
        self.assertEqual(episode.air_date, date_to_test)
        self.assertEqual(episode.overview, 'test episode overview 1')
        self.assertEqual(episode.runtime, 25)
        self.assertEqual(episode.still_path, '/test-episode-still-path-1')
