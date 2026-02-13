from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from auth_app.models import UserProfile
from profile_app.api.serializers import ProfileSerializer




class ProfileDetailView(RetrieveUpdateAPIView):
    """
    Detail and update endpoint for a single UserProfile.

    Supported operations:
    - GET   → Retrieve profile information
    - PATCH → Partially update the profile
    - PUT   → Fully update the profile

    Access:
    - Lookup via pk (Primary Key)
    - Uses ProfileSerializer
    """

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "pk"


class CustomerListView(ListAPIView):
    """
    Lists all profiles of type CUSTOMER.

    Notes:
    - Pagination is disabled (pagination_class = None)
    - Uses ProfileSerializer
    """

    pagination_class = None
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Returns only Customer profiles.
        """
        return UserProfile.objects.filter(
            type=UserProfile.UserType.CUSTOMER
        )


class BusinessListView(ListAPIView):
    """
    Lists all profiles of type BUSINESS.

    Notes:
    - Pagination is disabled (pagination_class = None)
    - Uses ProfileSerializer
    """

    pagination_class = None
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Returns only Business profiles.
        """
        return UserProfile.objects.filter(
            type=UserProfile.UserType.BUSINESS
        )
