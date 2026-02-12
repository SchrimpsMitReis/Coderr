from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review
from django.db.models import Count, Avg

class BaseInfoView(APIView):
    """
    Liefert aggregierte Plattform-Basisinformationen.

    Enthaltene Kennzahlen:
    - Anzahl Reviews
    - Durchschnittliche Bewertung
    - Anzahl Business-Profile
    - Anzahl Angebote
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Aggregiert systemweite Statistiken.
        """

        review_stats = Review.objects.aggregate(
            review_count=Count("id"),
            average_rating=Avg("rating")
        )

        data = {
            "review_count": review_stats["review_count"] or 0,
            "average_rating": review_stats["average_rating"] or 0,
            "business_profile_count": self._get_business_profile_count(),
            "offer_count": self._get_offer_count(),
        }

        return Response(data)

    def _get_business_profile_count(self):
        """Zählt Profile mit Typ BUSINESS."""
        return UserProfile.objects.filter(
            type=UserProfile.UserType.BUSINESS
        ).count()

    def _get_offer_count(self):
        """Zählt alle Angebote."""
        return Offer.objects.count()

