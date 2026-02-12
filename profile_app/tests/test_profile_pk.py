from django.urls import reverse
from rest_framework import status


from auth_app.models import UserProfile
from general_app.tests.base import AuthenticatedAPITestCaseCustomer



class TestSingleProfileHappy(AuthenticatedAPITestCaseCustomer):
    """
    Tests für Detail- und Update-Endpoint eines einzelnen Profils.
    """

    def setUp(self):
        super().setUp()
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.url = reverse(
            "single-user-profile-info",
            kwargs={"pk": self.user_profile.id},
        )

    def test_get_single_profile_returns_expected_fields(self):
        """
        GET sollte Status 200 liefern und alle erwarteten Felder enthalten.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = [
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        ]

        for field in expected_fields:
            self.assertIn(field, response.data)
            self.assertIsNotNone(response.data[field])

    def test_patch_single_profile_updates_fields(self):
        """
        PATCH sollte die Felder aktualisieren und Status 200 liefern.
        """
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }

        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Überprüfen, ob Werte wirklich geändert wurden
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

class TestUserListByTypeHappy(AuthenticatedAPITestCaseCustomer):
    """
    Tests für Profile-Listen nach Typ (Customer / Business).
    """

    def test_get_business_list_returns_profiles(self):
        url = reverse("business-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

        for profile in response.data:
            self.assertEqual(profile["type"], UserProfile.UserType.BUSINESS)

    def test_get_customer_list_returns_profiles(self):
        url = reverse("customer-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

        for profile in response.data:
            self.assertEqual(profile["type"], UserProfile.UserType.CUSTOMER)            
# class test_single_profile_happy(AuthenticatedAPITestCaseCustomer):

#     def setUp(self):
#         super().setUp()
#         self.url = reverse('single-user-profile-info',
#                            kwargs={"pk": self.user.id})

#     def test_get_single_profile(self):
#         fields = ['first_name', 'last_name', 'location',
#                   'tel', 'description', 'working_hours']
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         for field in fields:
#             self.assertNotEqual(response.data[f'{field}'], None)

#     def test_patch_single_profile(self):
#         data = {
#             "first_name": "Max",
#             "last_name": "Mustermann",
#             "location": "Berlin",
#             "tel": "987654321",
#             "description": "Updated business description",
#             "working_hours": "10-18",
#             "email": "new_email@business.de"
#         }
#         response = self.client.patch(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# class test_userlist_by_type_happy(AuthenticatedAPITestCaseCustomer):

#     def setUp(self):
#         super().setUp()
    
#     def test_get_business_list(self):
#         url = reverse('business-user-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_customer_list(self):
#         url = reverse('customer-user-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

