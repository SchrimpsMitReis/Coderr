from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenificatedAPITestCase






class LoginTestHappy(UnauthenificatedAPITestCase):
    """
    Happy-Path Tests für den Login-Endpoint.

    Erwartetes Verhalten:
    - Korrekte Credentials führen zu HTTP 200.
    - Response enthält Token und User-Daten.
    """

    def setUp(self):
        """
        Erstellt vor jedem Test einen gültigen User
        mit bekanntem Passwort.
        """
        super().setUp()
        self.user = self.create_user_object()

    @tag('happy')
    def test_user_login(self):
        """
        Prüft, ob sich ein User mit gültigen Credentials einloggen kann.
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

        # Überprüft, ob alle erwarteten Response-Felder vorhanden sind
        for key in ["token", "username", "email", "user_id"]:
            self.assertIn(key, response.data)
    

class LoginTestUnhappy(UnauthenificatedAPITestCase):
    """
    Unhappy-Path Tests für den Login-Endpoint.

    Erwartetes Verhalten:
    - Falsches Passwort führt zu HTTP 400.
    """

    def setUp(self):
        super().setUp()
        self.user = self.create_user_object()

    @tag('unhappy')
    def test_user_login_wrong_password(self):
        """
        Prüft, ob ein falsches Passwort korrekt abgewiesen wird.
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