from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from core.tests.base import UnauthenificatedAPITestCase


class RegistrationHappyTest(UnauthenificatedAPITestCase):

    def setUp(self):
        super().setUp()
    @tag('happy')
    def test_register_user_happy(self):
        url = reverse('user-registration')
        data = self.create_user_data()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)


class RegistrationUnhappyTest(APITestCase):
    
    @tag('unhappy')    
    def test_send_wrong_data(self):
        url = reverse('user-registration')
        data = {
            "ushername": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
    
    @tag('unhappy')
    def test_send_different_passwords(self):
        url = reverse('user-registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "exampasdfasdfalePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @tag('unhappy')
    def test_send_wrong_type(self):
        url = reverse('user-registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "Mitarbeiter"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @tag('unhappy')
    def test_send_missing_data(self):
        url = reverse('user-registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)
    
    @tag('unhappy')
    def test_register_user_again(self):
        url = reverse('user-registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type":"business"
        }
        response = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    