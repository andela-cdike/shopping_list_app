from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LoginTestSuite(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.client = Client()

    def test_login_view(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
