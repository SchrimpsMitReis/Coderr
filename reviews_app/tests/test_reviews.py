from rest_framework import status
from django.urls import reverse
from general_app.tests.base import AuthenticatedAPITestCaseCustomer, AuthenticatedAPITestCaseBusiness
from orders_app.models import Orders
from django.test import tag

class TestReviewsCustomer(AuthenticatedAPITestCaseCustomer):
    """
    Tests für Reviews aus Sicht eines CUSTOMER-Users.

    Abgedeckte Fälle:
    - Liste abrufen (Schema prüfen)
    - Filter nach business_user_id (Treffer / keine Treffer)
    - Review erstellen (POST)
    - Duplikat-Review verhindern (1 Review pro reviewer+business_user)
    - Review aktualisieren (PATCH)
    """

    @tag("happy")
    def test_list_reviews_returns_expected_schema(self):
        expected_keys = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        url = reverse("reviews-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            for key in expected_keys:
                self.assertIn(key, item)

    @tag("happy")
    def test_list_filter_by_business_user_returns_200(self):
        url = reverse("reviews-list")
        response = self.client.get(url, {"business_user_id": self.user_business.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("happy")
    def test_list_filter_by_unknown_business_user_returns_empty_list(self):
        url = reverse("reviews-list")
        response = self.client.get(url, {"business_user_id": 999999})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @tag("happy")
    def test_post_review_creates_review(self):
        url = reverse("reviews-list")
        data = {
            "business_user": self.user_business.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Optional: sicherstellen, dass reviewer automatisch gesetzt wurde
        self.assertEqual(response.data.get("reviewer"), self.user.id)

    @tag("unhappy")
    def test_post_duplicate_review_is_rejected(self):
        url = reverse("reviews-list")
        data = {
            "business_user": self.user_business.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        first = self.client.post(url, data, format="json")
        second = self.client.post(url, data, format="json")

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("happy")
    def test_patch_single_review_updates_fields(self):
        url = reverse("reviews-detail", kwargs={"pk": self.review_1.id})
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!",
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optional: Rückgabe prüfen (falls Serializer das Feld zurückgibt)
        self.assertEqual(response.data.get("rating"), 5)
        self.assertEqual(response.data.get("description"), "Noch besser als erwartet!")


class TestReviewsBusiness(AuthenticatedAPITestCaseBusiness):
    """
    Tests für Reviews aus Sicht eines BUSINESS-Users.

    Erwartung:
    - BUSINESS darf keine Reviews erstellen (POST -> 403),
      da Reviews von Kunden abgegeben werden.
    """

    @tag("unhappy")
    def test_post_review_as_business_is_forbidden(self):
        url = reverse("reviews-list")
        data = {
            "business_user": self.user_business.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
