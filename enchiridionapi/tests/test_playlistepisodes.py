from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Playlist, Episode, PlaylistEpisode

class PlaylistEpisodeTest(TestCase):
    """ Test module for PlaylistEpisode model """

    def setUp(self):
        user = User.objects.create_user(username='test_user', password='password')
        playlist = Playlist.objects.create(
            user=user,
            name='test playlist',
            description='this is a test playlist')
        episode = Episode.objects.create(
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
        PlaylistEpisode.objects.create(
            episode=episode,
            playlist=playlist,
            order_number=1
        )
        self.playlist=playlist
        self.episode=episode

    def test_playlistepisode(self):
        playlistepisode=PlaylistEpisode.objects.get(episode=self.episode, playlist=self.playlist, order_number=1)
        self.assertEqual(playlistepisode.episode, self.episode)
        self.assertEqual(playlistepisode.playlist, self.playlist)
        self.assertEqual(playlistepisode.order_number, 1)