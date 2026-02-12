import django_filters
from reviews_app.models import Review


class ReviewFilter(django_filters.FilterSet):
    """
    FilterSet für Review-Listenendpunkte.

    Ermöglicht Filterung nach:
    - business_user_id  -> Reviews zu einem bestimmten Business
    - reviewer_id       -> Reviews eines bestimmten Reviewers (Customers)

    Verwendungsbeispiel:
        /api/reviews/?business_user_id=5
        /api/reviews/?reviewer_id=12
    """

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