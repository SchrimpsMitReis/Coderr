from rest_framework import status
from django.urls import reverse
from general_app.tests.base import AuthenificatedAPITestCaseCustomer, AuthenificatedAPITestCaseBusiness
from orders_app.models import Orders







from general_app.tests.base import AuthenificatedAPITestCaseCustomer


class test_order_count(AuthenificatedAPITestCaseCustomer):
    


    def test_inprogress_order_count(self):
        url = reverse('order-count-inprogress', kwargs={'pk': self.user_business.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_complete_order_count(self):
        url = reverse('order-count-complete', kwargs={'pk': self.user_business.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)