from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review



class BaseInfoView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request):
        reviews = Review.objects.all()
        review_count = reviews.count()
        business_profile_count = UserProfile.objects.filter(type=UserProfile.UserType.BUSINESS).count()
        average_rating = self.get_average_rating(reviews, review_count)
        offer_count = Offer.objects.all().count()
        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }
        return Response(data)

    def get_average_rating(self, reviews, count):
        if count == 0:
            return 0

        total = sum(review.rating for review in reviews)
        return total / count
    

