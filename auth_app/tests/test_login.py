from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenificatedAPITestCase






class LoginTestHappy(UnauthenificatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user_object()

    @tag('happy')
    def test_user_login(self):
        keys = ["token", "username","email","user_id",]
        url = reverse("user-login")
        data = {
                "username": self.user.username,
                "password": "Password123!"  
            }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in keys:
            self.assertIn(key, response.data)

class LoginTestUnhappy(UnauthenificatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user_object()
        
    @tag('unhappy')
    def test_user_login_wrong_password(self):
        url = reverse("user-login")
        data = {
                "username": self.user.username,
                "password": "Password123"  
            }
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

