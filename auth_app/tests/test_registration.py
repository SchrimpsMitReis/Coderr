from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenificatedAPITestCase


class RegistrationHappyTest(UnauthenificatedAPITestCase):
    """
    Happy-Path Tests für den Registration-Endpoint.

    Erwartetes Verhalten:
    - Gültige Daten führen zu HTTP 201.
    - Response enthält Auth-Token und User-ID.
    """

    @tag("happy")
    def test_register_user_returns_token_and_user_id(self):
        url = reverse("user-registration")
        data = self.create_user_data()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)

class RegistrationUnhappyTest(UnauthenificatedAPITestCase):
    """
    Unhappy-Path Tests für den Registration-Endpoint.

    Erwartetes Verhalten:
    - Ungültige Daten führen zu HTTP 400.
    - Response enthält feldbezogene Fehlermeldungen.
    """

    def _post_registration(self, data):
        """Hilfsfunktion, damit Tests kurz und konsistent bleiben."""
        url = reverse("user-registration")
        return self.client.post(url, data, format="json")

    @tag("unhappy")
    def test_missing_username_field_returns_400_and_username_error(self):
        """
        Wenn 'username' fehlt (z.B. Tippfehler im Feldnamen),
        muss die API das als Pflichtfeld-Fehler zurückgeben.
        """
        data = {
            "ushername": "exampleUsername",  # absichtlich falsch
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
        """Wenn Passwörter nicht übereinstimmen, muss Validierung fehlschlagen."""
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "differentPassword",
            "type": "customer",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Optional, falls du das explizit zurückgibst:
        self.assertIn("repeated_password", response.data)

    @tag("unhappy")
    def test_invalid_type_returns_400_and_type_error(self):
        """Ungültiger Choice-Wert für 'type' muss 400 liefern."""
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "Mitarbeiter",
        }

        response = self._post_registration(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)

    @tag("unhappy")
    def test_missing_type_returns_400_and_type_error(self):
        """Wenn 'type' fehlt, muss ein Pflichtfeld-Fehler zurückkommen."""
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
    def test_register_same_user_twice_second_fails(self):
        """
        Username/E-Mail müssen eindeutig sein.
        Erstes Register: 201
        Zweites Register mit gleichen Daten: 400
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
        # Optional stärker:
        self.assertTrue("username" in second.data or "email" in second.data)