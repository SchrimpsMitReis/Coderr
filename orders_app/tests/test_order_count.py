from rest_framework import status
from django.urls import reverse
from general_app.tests.base import AuthenticatedAPITestCaseCustomer, AuthenticatedAPITestCaseBusiness
from orders_app.models import Orders








class TestOrderCount(AuthenticatedAPITestCaseCustomer):
    """
        Tests for the Order count endpoints.
    
        Expected behavior (based on test data from the BaseTestCase):
        - There are 2 Orders in status IN_PROGRESS for the Business user.
        - There are 0 Orders in status COMPLETED.
        """    
    def test_inprogress_order_count_returns_correct_value(self):
        url = reverse("order-count-inprogress", kwargs={"pk": self.user_business.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("order_count", response.data)
        self.assertIsInstance(response.data["order_count"], int)
        self.assertEqual(response.data["order_count"], 2)

    def test_completed_order_count_returns_correct_value(self):
        url = reverse("order-count-complete", kwargs={"pk": self.user_business.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("completed_order_count", response.data)
        self.assertIsInstance(response.data["completed_order_count"], int)
        self.assertEqual(response.data["completed_order_count"], 0)