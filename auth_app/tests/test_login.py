from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenticatedAPITestCase






class LoginTestHappy(UnauthenticatedAPITestCase):
    """
    Happy-path tests for the login endpoint.

    Expected behavior:
    - Valid credentials result in HTTP 200.
    - The response contains the authentication token and user data.
    """

    def setUp(self):
        """
        Creates a valid user with a known password
        before each test.
        """
        super().setUp()
        self.user = self._create_user()

    @tag("happy")
    def test_user_login(self):
        """
        Verifies that a user can successfully log in
        using valid credentials.
        """
        url = reverse("user-login")

        response = self.client.post(
            url,
            {
                "username": self.user.username,
                "password": "Password123!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in ["token", "username", "email", "user_id"]:
            self.assertIn(key, response.data)


class LoginTestUnhappy(UnauthenticatedAPITestCase):
    """
    Unhappy-path tests for the login endpoint.

    Expected behavior:
    - An incorrect password results in HTTP 400.
    """

    def setUp(self):
        super().setUp()
        self.user = self._create_user()

    @tag("unhappy")
    def test_user_login_wrong_password(self):
        """
        Verifies that an incorrect password
        is properly rejected.
        """
        url = reverse("user-login")

        response = self.client.post(
            url,
            {
                "username": self.user.username,
                "password": "WrongPassword123",
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
