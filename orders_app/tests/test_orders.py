from rest_framework import status
from django.urls import reverse
from core.tests.base import AuthenificatedAPITestCaseCustomer, AuthenificatedAPITestCaseBusiness
from orders_app.models import Orders



class test_orders_business(AuthenificatedAPITestCaseBusiness):

    def test_post_order_unhappy(self):
        url = reverse("orders-list")
        data = {
            'offer_detail_id' : self.offer_detail_basic_1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order_1.id})
        data = {
            'status': Orders.StatusType.COMPLETED
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class test_orders_customer(AuthenificatedAPITestCaseCustomer):

    def test_post_order_unhappy(self):
        url = reverse("orders-list")
        data = {
            'offer_detail_id' : self.offer_detail_basic_1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order_1})
        data = {
            'status': Orders.StatusType.COMPLETED
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order(self):
        url = reverse('orders-detail', kwargs={'pk': self.order_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

