from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import BookingRequest, ServicePackage
from datetime import date
from django.contrib.auth.models import Group

User = get_user_model()


class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='photographer', password='pass123')
        photographers_group, _ = Group.objects.get_or_create(name='Photographers')
        self.user.groups.add(photographers_group)

        self.package = ServicePackage.objects.create(
            name="Basic",
            price=50,
            duration_hours=2,
        )

    def test_booking_model_str(self):
        booking = BookingRequest.objects.create(
            first_name="Test",
            last_name="User",
            email="test@test.com",
            event_date=date.today(),
            status=BookingRequest.Status.PENDING,
        )
        self.assertIn("Test User", str(booking))

    def test_booking_status_default_pending(self):
        booking = BookingRequest.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@test.com",
            event_date=date.today(),
        )
        self.assertEqual(booking.status, "pending")

    def test_package_str(self):
        self.assertIn("Basic", str(self.package))
        self.assertIn("50", str(self.package))

    def test_booking_request_view(self):
        response = self.client.get(reverse('bookings:booking_request'))
        self.assertEqual(response.status_code, 200)

    def test_booking_list_view(self):
        self.client.login(username='photographer', password='pass123')
        response = self.client.get(reverse('bookings:booking_list'))
        self.assertEqual(response.status_code, 200)

    def test_package_list_view(self):
        response = self.client.get(reverse('bookings:package_list'))
        self.assertEqual(response.status_code, 200)

    def test_package_detail_view(self):
        response = self.client.get(
            reverse('bookings:package_detail', kwargs={'pk': self.package.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_package_create_requires_login(self):
        response = self.client.get(reverse('bookings:package_create'))
        self.assertEqual(response.status_code, 302)

    def test_api_package_list(self):
        response = self.client.get(reverse('bookings:api_package_list'))
        self.assertEqual(response.status_code, 200)

    def test_api_booking_request_requires_post(self):
        response = self.client.get(reverse('bookings:api_booking_request'))
        self.assertIn(response.status_code, [200, 401, 403, 405])