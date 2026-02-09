from rest_framework import status
from django.urls import reverse
from core.tests.base import AuthenificatedAPITestCaseCustomer, AuthenificatedAPITestCaseBusiness
from orders_app.models import Orders
from django.test import tag

class test_reviews_Customer(AuthenificatedAPITestCaseCustomer):

    @tag('happy')
    def test_list_reviews(self):
        keys = ['id', 'business_user', 'reviewer', 'rating',
                'description', 'created_at', 'updated_at']
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for result in response.data:
            for key in keys:
                self.assertIn(key, result)

    @tag('happy')
    def test_list_filter_business_user(self):
        url = reverse('reviews-list')
        response = self.client.get(url, {"business_user_id": self.user_business.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @tag('happy')
    def test_list_filter_business_user_unknown(self):
        url = reverse('reviews-list')
        response = self.client.get(url, {"business_user_id": 999999})
        
        items = response.data
        print(items)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(items), 0)
     

    @tag('happy')
    def test_post_reviews(self):
        url = reverse('reviews-list')
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('unhappy')
    def test_post_two_reviews(self):
        url = reverse('reviews-list')
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url,data,format='json')
        response2 = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('happy')
    def test_patch_single_review(self):
        url = reverse('reviews-detail', kwargs={'pk': self.review_1.id})
        data = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class test_reviews_Business(AuthenificatedAPITestCaseBusiness):
    @tag('unhappy')
    def test_post_reviews_unhappy(self):
        url = reverse('reviews-list')
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


