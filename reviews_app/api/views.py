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
    ViewSet für Reviews (CRUD).

    Features:
    - Auth erforderlich (IsAuthenticated)
    - Zusätzliche Regeln über ReviewPermission (z.B. wer updaten/löschen darf)
    - Keine Pagination (pagination_class = None)
    - Filterung via ReviewFilter:
        - business_user_id
        - reviewer_id
    - Ordering:
        - updated_at
        - rating
      Default: neueste zuerst (-updated_at)

    Create-Verhalten:
    - reviewer wird serverseitig aus request.user gesetzt (perform_create)
    """

    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated, ReviewPermission]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter

    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def perform_create(self, serializer):
        """
        Setzt den Reviewer automatisch auf den eingeloggten User.

        Dadurch kann der Client das Feld `reviewer` nicht fälschen.
        """
        serializer.save(reviewer=self.request.user)