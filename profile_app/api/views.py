from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from auth_app.models import UserProfile
from profile_app.api.serializers import ProfileSerializer




class ProfileDetailView(RetrieveUpdateAPIView):
    """
    Detail- und Update-Endpoint für ein einzelnes UserProfile.

    Funktionen:
    - GET     -> Profilinformationen abrufen
    - PATCH   -> Profil teilweise aktualisieren
    - PUT     -> Profil vollständig aktualisieren

    Zugriff:
    - Standardmäßig über pk (Primary Key)
    - Verwendet ProfileSerializer
    """

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "pk"


class CustomerListView(ListAPIView):
    """
    Listet alle Profile vom Typ CUSTOMER.

    Hinweis:
    - Keine Pagination (pagination_class = None)
    - Verwendet ProfileSerializer
    """

    pagination_class = None
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Liefert ausschließlich Customer-Profile.
        """
        return UserProfile.objects.filter(
            type=UserProfile.UserType.CUSTOMER
        )


class BusinessListView(ListAPIView):
    """
    Listet alle Profile vom Typ BUSINESS.

    Hinweis:
    - Keine Pagination (pagination_class = None)
    - Verwendet ProfileSerializer
    """

    pagination_class = None
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Liefert ausschließlich Business-Profile.
        """
        return UserProfile.objects.filter(
            type=UserProfile.UserType.BUSINESS
        )