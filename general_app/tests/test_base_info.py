from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenticatedAPITestCase




class BaseInfoTest(UnauthenticatedAPITestCase):
    """
    Tests für den BaseInfo-Endpoint.

    Erwartetes Verhalten:
    - GET /base-info/ liefert HTTP 200
    - Response enthält alle erwarteten Statistik-Felder
    - Werte sind numerisch
    """

    @tag("happy")
    def test_get_base_info_returns_expected_keys_and_numeric_values(self):
        url = reverse("base-info")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = [
            "review_count",
            "average_rating",
            "business_profile_count",
            "offer_count",
        ]

        for key in expected_keys:
            self.assertIn(key, response.data)
            self.assertIsInstance(response.data[key], (int, float))