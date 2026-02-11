from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from general_app.tests.base import UnauthenificatedAPITestCase




class test_base_info(UnauthenificatedAPITestCase):

    url = reverse('base-info')
    data_keys = [ "review_count","average_rating","business_profile_count","offer_count"]

    @tag('unhappy')
    def test_get_base_info(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.data_keys:
            self.assertIn(key, response.data)
