import django_filters
from reviews_app.models import Review


class ReviewFilter(django_filters.FilterSet):
    """
    FilterSet for review list endpoints.
    
    Allows filtering by:
    - business_user_id → Reviews for a specific Business user
    - reviewer_id      → Reviews written by a specific reviewer (Customer)
    
    Example usage:
        /api/reviews/?business_user_id=5
        /api/reviews/?reviewer_id=12    """

    business_user_id = django_filters.NumberFilter(
        field_name="business_user_id"
    )

    reviewer_id = django_filters.NumberFilter(
        field_name="reviewer_id"
    )

class Meta:
        model = Review
        fields = {
            "business_user": ["exact"],
            "reviewer": ["exact"],
        }