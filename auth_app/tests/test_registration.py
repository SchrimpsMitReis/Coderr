from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenticatedAPITestCase


class RegistrationHappyTest(UnauthenticatedAPITestCase):
    """
    Happy-path tests for the registration endpoint.

    Expected behavior:
    - Valid data results in HTTP 201.
    - The response contains an authentication token and user_id.
    """

    @tag("focused")
    def test_register_user_returns_token_and_user_id(self):
        url = reverse("user-registration")
        data = self.create_user_data()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)


class RegistrationUnhappyTest(UnauthenticatedAPITestCase):
    """
    Unhappy-path tests for the registration endpoint.

    Expected behavior:
    - Invalid input results in HTTP 400.
    - The response contains field-level validation errors.
    """

    def _post_registration(self, data):
        """Helper method to keep tests concise and consistent."""
        url = reverse("user-registration")
        return self.client.post(url, data, format="json")

    @tag("unhappy")
    def test_missing_username_field_returns_400_and_username_error(self):
        """
        If 'username' is missing (e.g., due to a typo in the field name),
        the API must return a required-field validation error.
        """
        data = {
            "ushername": "exampleUsername",  # intentionally incorrect
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)  # "This field is required."

    @tag("unhappy")
    def test_different_passwords_returns_400_and_repeated_password_error(self):
        """Validation must fail if passwords do not match."""
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "differentPassword",
            "type": "customer",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("repeated_password", response.data)

    @tag("unhappy")
    def test_invalid_type_returns_400_and_type_error(self):
        """An invalid choice value for 'type' must return HTTP 400."""
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "Employee",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)

    @tag("unhappy")
    def test_missing_type_returns_400_and_type_error(self):
        """If 'type' is missing, a required-field validation error must be returned."""
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)

    @tag("unhappy")
    def test_register_same_user_twice_second_attempt_fails(self):
        """
        Username and email must be unique.
        First registration: 201
        Second registration with same data: 400
        """
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business",
        }

        first = self._post_registration(data)
        second = self._post_registration(data)

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("username" in second.data or "email" in second.data)
