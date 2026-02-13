from reviews_app.api.filter import ReviewFilter
from reviews_app.api.permissions import ReviewPermission
from reviews_app.api.serializers import ReviewListSerializer
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

class ReviewViewSet(ModelViewSet):
    """
    ViewSet for Reviews (CRUD).
    
    Features:
    - Authentication required (IsAuthenticated)
    - Additional rules enforced via ReviewPermission
      (e.g., who may update or delete)
    - No pagination (pagination_class = None)
    - Filtering via ReviewFilter:
        - business_user_id
        - reviewer_id
    - Ordering support:
        - updated_at
        - rating
      Default: newest first (-updated_at)
    
    Create behavior:
    - reviewer is set server-side from request.user
      (via perform_create)    """
    
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ReviewPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter

    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)