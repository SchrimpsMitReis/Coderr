from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review
from django.db.models import Count, Avg

class BaseInfoView(APIView):
    """
    Returns aggregated platform-level statistics.

    Included metrics:
    - Total number of reviews
    - Average rating
    - Number of business profiles
    - Number of offers
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Aggregates system-wide statistics.
        """

        review_stats = Review.objects.aggregate(
            review_count=Count("id"),
            average_rating=Avg("rating"),
        )

        data = {
            "review_count": review_stats["review_count"] or 0,
            "average_rating": review_stats["average_rating"] or 0,
            "business_profile_count": self._get_business_profile_count(),
            "offer_count": self._get_offer_count(),
        }

        return Response(data)

    def _get_business_profile_count(self):
        """Returns the number of profiles with type BUSINESS."""
        return UserProfile.objects.filter(
            type=UserProfile.UserType.BUSINESS
        ).count()

    def _get_offer_count(self):
        """Returns the total number of offers."""
        return Offer.objects.count()
