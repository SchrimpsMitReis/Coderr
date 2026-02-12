

from django.test import tag
from rest_framework import status

from django.urls import reverse
from general_app.tests.base import AuthenticatedAPITestCaseCustomer, AuthenticatedAPITestCaseBusiness

class TestOffersCustomer(AuthenticatedAPITestCaseCustomer):
    """
    Customer-spezifische Tests für Offers.

    Erwartung:
    - GET list funktioniert (200) + Pagination + korrekte Response-Struktur
    - POST Offer ist nicht erlaubt (Business required) -> 400 (oder 403 je nach Implementierung)
    """

    @tag("happy")
    def test_get_offers_list_returns_paginated_results(self):
        url = reverse("offers-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_pagination_schema(response.data)
        self._assert_offer_list_schema(response.data["results"])

    @tag("unhappy")
    def test_post_offer_as_customer_fails(self):
        url = reverse("offers-list")
        response = self.client.post(url, self._offer_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _offer_payload(self):
        """Standard-Payload für Offer-Erstellung."""
        return {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100,
                 "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200,
                 "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500,
                 "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

    def _assert_pagination_schema(self, data):
        """Prüft Standard-Pagination-Felder."""
        for key in ["count", "next", "previous", "results"]:
            self.assertIn(key, data)

    def _assert_offer_list_schema(self, results):
        """Prüft Schema der Offer-Objekte in der List-Response."""
        for offer in results:
            for key in [
                "user", "title", "image", "description",
                "details", "min_price", "min_delivery_time", "user_details"
            ]:
                self.assertIn(key, offer)

            for detail in offer["details"]:
                for key in ["id", "url"]:
                    self.assertIn(key, detail)

            for key in ["first_name", "last_name", "username"]:
                self.assertIn(key, offer["user_details"])

class TestOffersBusiness(AuthenticatedAPITestCaseBusiness):
    """
    Business-spezifische Tests für Offers.

    Erwartung:
    - POST create funktioniert (201)
    - PATCH update funktioniert (200)
    - DELETE funktioniert (204) und Objekt ist danach nicht mehr abrufbar
    - OfferDetail retrieve funktioniert (200)
    """

    @tag("happy")
    def test_post_offer_as_business_creates_offer(self):
        url = reverse("offers-list")
        response = self.client.post(url, self._offer_payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag("happy")
    def test_patch_offer_updates_offer_and_details(self):
        url = reverse("offers-detail", kwargs={"pk": self.offer_1.id})
        response = self.client.patch(url, self._patch_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ["id", "title", "image", "description", "details"]:
            self.assertIn(key, response.data)

        for detail in response.data["details"]:
            for key in ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]:
                self.assertIn(key, detail)

    @tag("happy")
    def test_delete_offer_removes_offer(self):
        url = reverse("offers-detail", kwargs={"pk": self.offer_1.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # optional: stellt sicher, dass es wirklich weg ist
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

    @tag("happy")
    def test_get_offerdetail_single(self):
        url = reverse("offerdetail-detail", kwargs={"pk": self.offer_detail_basic_1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]:
            self.assertIn(key, response.data)

    def _offer_payload(self):
        """Standard-Payload für Offer-Erstellung."""
        return {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {"title": "Basic Design", "revisions": 2, "delivery_time_in_days": 5, "price": 100,
                 "features": ["Logo Design", "Visitenkarte"], "offer_type": "basic"},
                {"title": "Standard Design", "revisions": 5, "delivery_time_in_days": 7, "price": 200,
                 "features": ["Logo Design", "Visitenkarte", "Briefpapier"], "offer_type": "standard"},
                {"title": "Premium Design", "revisions": 10, "delivery_time_in_days": 10, "price": 500,
                 "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"], "offer_type": "premium"},
            ],
        }

    def _patch_payload(self):
        """Payload für partial_update: aktualisiert gezielt das basic-Detail."""
        return {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                }
            ],
        }