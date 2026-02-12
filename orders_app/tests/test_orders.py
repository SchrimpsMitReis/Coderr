from rest_framework import status
from django.urls import reverse
from general_app.tests.base import AuthenticatedAPITestCaseCustomer, AuthenticatedAPITestCaseBusiness
from orders_app.models import Orders



class TestOrdersBusiness(AuthenticatedAPITestCaseBusiness):
    """
    Tests für Orders aus Sicht eines BUSINESS-Users.

    Erwartung:
    - BUSINESS darf keine Orders erstellen (POST) -> 403
    - BUSINESS darf Status eigener Orders ändern -> 200
    - DELETE ist nur staff/admin -> 403
    """

    def test_business_cannot_create_order(self):
        url = reverse("orders-list")
        response = self.client.post(
            url,
            {"offer_detail_id": self.offer_detail_basic_1.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_business_can_patch_own_order_status(self):
        url = reverse("orders-detail", kwargs={"pk": self.order_1.id})
        response = self.client.patch(
            url,
            {"status": Orders.StatusType.COMPLETED},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], Orders.StatusType.COMPLETED)

    def test_business_cannot_delete_order(self):
        url = reverse("orders-detail", kwargs={"pk": self.order_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestOrdersCustomer(AuthenticatedAPITestCaseCustomer):
    """
    Tests für Orders aus Sicht eines CUSTOMER-Users.

    Erwartung:
    - CUSTOMER darf Orders erstellen -> 201
    - CUSTOMER darf Orders nicht patchen -> 403
    - DELETE ist nur staff/admin -> 403
    """

    def test_customer_can_create_order(self):
        url = reverse("orders-list")
        response = self.client.post(
            url,
            {"offer_detail_id": self.offer_detail_basic_1.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Optional: Response-Struktur prüfen
        for key in ["id", "status", "customer_user", "business_user", "title", "revisions","delivery_time_in_days","price","features","offer_type","created_at"]:
            self.assertIn(key, response.data)

    def test_customer_cannot_patch_order(self):
        url = reverse("orders-detail", kwargs={"pk": self.order_1.id})
        response = self.client.patch(
            url,
            {"status": Orders.StatusType.COMPLETED},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_delete_order(self):
        url = reverse("orders-detail", kwargs={"pk": self.order_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


