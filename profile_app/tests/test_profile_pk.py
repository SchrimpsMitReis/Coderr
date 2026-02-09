from django.urls import reverse
from rest_framework import status


from core.tests.base import AuthenificatedAPITestCaseCustomer


class test_single_profile_happy(AuthenificatedAPITestCaseCustomer):

    def setUp(self):
        super().setUp()
        self.url = reverse('single-user-profile-info',
                           kwargs={"pk": self.user.id})

    def test_get_single_profile(self):
        fields = ['first_name', 'last_name', 'location',
                  'tel', 'description', 'working_hours']
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in fields:
            self.assertNotEqual(response.data[f'{field}'], None)

    def test_patch_single_profile(self):
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class test_userlist_by_type_happy(AuthenificatedAPITestCaseCustomer):

    def setUp(self):
        super().setUp()
    
    def test_get_business_list(self):
        url = reverse('business-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_list(self):
        url = reverse('customer-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

