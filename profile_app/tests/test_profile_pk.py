from django.urls import reverse
from rest_framework import status


from auth_app.models import UserProfile
from general_app.tests.base import AuthenticatedAPITestCaseCustomer



class TestSingleProfileHappy(AuthenticatedAPITestCaseCustomer):
    """
    Tests for the detail and update endpoint of a single profile.
    """

    def setUp(self):
        super().setUp()

        self.user_profile = UserProfile.objects.get(user=self.user)
        self.url = reverse(
            "single-user-profile-info",
            kwargs={"pk": self.user_profile.id},
        )

    def test_get_single_profile_returns_expected_fields(self):
        """
        GET should return HTTP 200 and include all expected fields.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = [
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        ]

        for field in expected_fields:
            self.assertIn(field, response.data)
            self.assertIsNotNone(response.data[field])

    def test_patch_single_profile_updates_fields(self):
        """
        PATCH should update the provided fields and return HTTP 200.
        """
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }

        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in data.items():
            self.assertEqual(response.data[key], value)


class TestUserListByTypeHappy(AuthenticatedAPITestCaseCustomer):
    """
    Tests for profile list endpoints filtered by user type (Customer / Business).
    """

    def test_get_business_list_returns_profiles(self):
        url = reverse("business-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

        for profile in response.data:
            self.assertEqual(profile["type"], UserProfile.UserType.BUSINESS)

    def test_get_customer_list_returns_profiles(self):
        url = reverse("customer-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

        for profile in response.data:
            self.assertEqual(profile["type"], UserProfile.UserType.CUSTOMER)
