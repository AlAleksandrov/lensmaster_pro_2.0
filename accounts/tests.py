from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='password123'
        )
        self.profile = Profile.objects.get(user=self.user)

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_requires_login(self):
        response = self.client.get(reverse('accounts:profile_detail'))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_detail_authenticated(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('accounts:profile_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_authenticated(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)

    def test_stats_requires_login(self):
        response = self.client.get(reverse('accounts:stats'))
        self.assertEqual(response.status_code, 302)

    def test_create_user(self):
        self.assertEqual(self.user.username, 'tester')
        self.assertTrue(self.user.is_active)

    def test_login_with_valid_credentials(self):
        logged_in = self.client.login(username='tester', password='password123')
        self.assertTrue(logged_in)

    def test_login_with_invalid_credentials(self):
        logged_in = self.client.login(username='tester', password='wrongpass')
        self.assertFalse(logged_in)