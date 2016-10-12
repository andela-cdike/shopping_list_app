from django.contrib.auth.models import User
from django.test import TestCase


class UserModelTestSuite(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@test.com', 'admin')

    def test_user_model(self):
        user = User.objects.get(username='admin')
        self.assertEqual(str(user), 'admin')
