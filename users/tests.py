from django.core import mail
from django.test import override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from travel.models import Destination

from .models import ActivityLog


class AuthAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="demo",
            email="demo@example.com",
            password="secret123",
        )

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_login_sends_otp_and_verifies_to_return_tokens(self):
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            {"username": "demo", "password": "secret123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent", response.data["detail"])
        self.assertEqual(len(mail.outbox), 1)

        otp_code = self.user.otps.latest("created_at").otp_code
        verify_url = reverse("verify-otp")
        verify_response = self.client.post(
            verify_url,
            {"username": "demo", "otp": otp_code},
            format="json",
        )

        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", verify_response.data)
        self.assertIn("refresh", verify_response.data)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_login_accepts_case_insensitive_username(self):
        login_url = reverse("login")
        response = self.client.post(
            login_url,
            {"username": "Demo", "password": "secret123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent", response.data["detail"])

    def test_authenticated_user_can_manage_posts(self):
        self.client.force_authenticate(user=self.user)
        create_url = reverse("post-list")
        create_response = self.client.post(
            create_url,
            {"title": "My first post", "description": "Hello world"},
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.activitylog_set.exists())

        post_id = create_response.data["id"]
        detail_url = reverse("post-detail", args=[post_id])
        update_response = self.client.patch(
            detail_url,
            {"title": "Updated title"},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_posts_list_supports_backend_search(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(
            reverse("post-list"),
            {"title": "Summer Escape", "description": "A tropical getaway"},
            format="json",
        )

        response = self.client.get(reverse("post-list"), {"search": "tropical"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Summer Escape")

    def test_logs_endpoint_returns_filtered_activity_logs(self):
        self.client.force_authenticate(user=self.user)
        ActivityLog.objects.create(user=self.user, action="Login", details="Login initiated")
        ActivityLog.objects.create(user=self.user, action="Create Post", details="Created a special post")

        response = self.client.get(reverse("activity-logs"), {"search": "special"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["details"], "Created a special post")

    def test_travel_list_supports_backend_search(self):
        Destination.objects.create(
            title="Santorini Escape",
            description="Breathtaking blue domes",
            country="Greece",
            city="Santorini",
            travel_category="Island",
            author=self.user,
        )

        response = self.client.get(reverse("destination-list"), {"search": "breathtaking"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Santorini Escape")
