

from django.test import tag
from rest_framework import status

from django.urls import reverse
from general_app.tests.base import AuthenificatedAPITestCaseCustomer, AuthenificatedAPITestCaseBusiness


class test_offers_customer(AuthenificatedAPITestCaseCustomer):

    def setUp(self):
        return super().setUp()
    
    @tag('happy')
    def test_get_offers_list_happy(self):
        url = reverse("offers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        for key in ["count", "next", "previous", "results"]:
            self.assertIn(key, data)

        for idx, offer in enumerate(data["results"], start=1):
            for key in [
                "user", "title", "image", "description",
                "details", "min_price", "min_delivery_time", "user_details"
            ]:
                self.assertIn(key, offer, f"Offer #{idx} missing key: {key}")

            for d_idx, detail in enumerate(offer["details"], start=1):
                for key in ["id", "url"]:
                    self.assertIn(
                        key, detail, f"Offer #{idx} detail #{d_idx} missing key: {key}")

            user_details = offer["user_details"]
            for key in ["first_name", "last_name", "username"]:
                self.assertIn(key, user_details,
                              f"Offer #{idx} user_details missing key: {key}")
    
    @tag('unhappy')
    def test_post_offers_unhappy(self):
        url = reverse("offers-list")
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class test_offers_business(AuthenificatedAPITestCaseBusiness):

    def setUp(self):
        return super().setUp()

    @tag('happy')
    def test_post_offers_happy(self):
        url = reverse("offers-list")
        data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('happy')
    def test_patch_offers_happy(self):
        url = reverse("offers-detail", kwargs={'pk': self.offer_1.id})
        data = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer"
                    ],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key in [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]:
            self.assertIn(key, response.data)

        for i, detail in enumerate(response.data['details']):
            for key in [
                "id",
                "title",
                "revisions",
                "delivery_time_in_days",
                "price",
                "features",
                "offer_type"]:
                self.assertIn(key, response.data['details'][i])
                
    @tag('happy')
    def test_delete_offers_happy(self):
        url = reverse("offers-detail", kwargs={'pk': self.offer_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    @tag('happy')
    def get_offerdetails_happy(self):
        url = reverse('offerdetail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)