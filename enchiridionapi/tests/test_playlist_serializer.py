from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.db.models import Count
from enchiridionapi.models import Playlist, Episode
from enchiridionapi.serializers import PlaylistSerializer

class PlaylistSerializerTest(TestCase):
    """ Test module for playlist serializer """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password')
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='test playlist name 1',
            description='test playlist description 1'
        )

        for i in range(1, 4):
            episode = Episode.objects.create(
                tmdb_id=i,
                series_id=1,
                series_name='test series name 1',
                season_number=1,
                episode_number=i,
                name='test episode name {}'.format(i),
                air_date='2000-01-{:02d}'.format(i),
                overview='test episode overview {}'.format(i),
                runtime=25,
                still_path='/test-episode-still-path-{}'.format(i)
            )
            self.playlist.episodes.add(episode, through_defaults={'order_number': i})

    def test_playlist_serializer(self):
        request = RequestFactory().get('/')
        request.user = self.user
        queryset = PlaylistSerializer.setup_eager_loading(Playlist.objects.annotate(likes_count=Count('like')))
        serializer = PlaylistSerializer(queryset, many=True, context={'request': request})
        data = serializer.data

        self.assertEqual(data[0]['id'], self.playlist.id)
        self.assertEqual(data[0]['user_id'], self.playlist.user.id)
        self.assertEqual(data[0]['name'], self.playlist.name)
        self.assertEqual(data[0]['description'], self.playlist.description)
        self.assertEqual(len(data[0]['episodes']), self.playlist.episodes.count())
        self.assertIn('likes_count', data[0])
        self.assertIn('is_liked', data[0])
