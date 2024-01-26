from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from unittest.mock import patch

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='password')

    def test_login_user(self):
        response = self.client.post('/login', {'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'valid')
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('access_token', response.cookies)
        self.assertIn('csrftoken', response.cookies)

    def test_verify_user(self):
        self.client.login(username='test_user', password='password')
        response = self.client.get('/verify')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='test_user', password='password')
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(datetime.datetime.strptime(response.cookies.get('refresh_token')['expires'], '%a, %d %b %Y %H:%M:%S GMT') < datetime.datetime.now())
        self.assertTrue(datetime.datetime.strptime(response.cookies.get('access_token')['expires'], '%a, %d %b %Y %H:%M:%S GMT') < datetime.datetime.now())
        self.assertTrue(datetime.datetime.strptime(response.cookies.get('csrftoken')['expires'], '%a, %d %b %Y %H:%M:%S GMT') < datetime.datetime.now())

class GoogleLoginTest(TestCase):
    @patch('requests.post')
    @patch('requests.get')
    def test_google_login(self, mock_get, mock_post):
        # Mock the response from Google's servers
        mock_post.return_value.json.return_value = {
            'access_token': 'access_token'
        }
        mock_get.return_value.json.return_value = {
            'email': 'test@example.com',
            'given_name': 'John',
            'family_name': 'Doe',
        }

        # Use the Django test client to simulate a POST request to the /google/login/ endpoint
        response = Client().post('/google/login', {'codeResponse': 'code'})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
