from rest_framework import status
from django.urls import reverse
from general_app.tests.base import AuthenticatedAPITestCaseCustomer, AuthenticatedAPITestCaseBusiness
from orders_app.models import Orders



class TestOrdersBusiness(AuthenticatedAPITestCaseBusiness):
    """
        Tests for Order endpoints from the perspective of a BUSINESS user.

        Expected behavior:
        - BUSINESS users are not allowed to create orders (POST) → 403
        - BUSINESS users may update the status of their own orders → 200
        - DELETE is restricted to staff/admin users → 403
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
        Tests for Order endpoints from the perspective of a CUSTOMER user.

        Expected behavior:
        - CUSTOMER users may create orders → 201
        - CUSTOMER users may not update orders → 403
        - DELETE is restricted to staff/admin users → 403
        """

    def test_customer_can_create_order(self):
        url = reverse("orders-list")
        response = self.client.post(
            url,
            {"offer_detail_id": self.offer_detail_basic_1.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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


