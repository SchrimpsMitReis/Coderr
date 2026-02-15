from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from offers_app.api.pagination import OfferPagination
from offers_app.api.permissions import OfferPermission
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferDetailSerializer, OfferFilterSerializer, OfferSerializer, OfferSerializerPostPatch, OfferSingleSerializer
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import ValidationError

class OfferViewSet(ModelViewSet):
    """
    ViewSet for Offers (CRUD).

    Features:
    - Authentication required (IsAuthenticated)
    - Pagination via OfferPagination
    - Search by title/description
    - Ordering (e.g., updated_at, min_price)
    - Query parameter filters:
        - creator_id: offers created by a specific user
        - min_price: minimum package price >= X
        - max_delivery_time: minimum delivery time <= X
    """

    queryset = Offer.objects.all()
    permission_classes = [OfferPermission]

    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    search_fields = ["title", "description"]

    ordering_fields = ["updated_at", "min_price"]
    ordering = ["updated_at"]

    def list(self, request, *args, **kwargs):
        filter_serializer = OfferFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data
        queryset = self.get_queryset()

        if "max_delivery_time" in filters:
            queryset = queryset.filter(
                details__delivery_time_in_days__lte=filters["max_delivery_time"]
            )

        if "min_price" in filters:
            queryset = queryset.filter(
                details__price__gte=filters["min_price"]
            )

        if "search" in filters:
            queryset = queryset.filter(title__icontains=filters["search"])

        self.queryset = queryset

        return super().list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        """
        Selects the appropriate serializer depending on the action:
        - create/update/partial_update: nested input (details included)
        - retrieve: detailed output
        - list: compact output with aggregations
        """
        if self.action in ["create", "update", "partial_update"]:
            return OfferSerializerPostPatch
        if self.action == "retrieve":
            return OfferSingleSerializer
        return OfferSerializer

    def get_queryset(self):
        """
        Adds aggregation annotations for filtering/ordering
        and applies query parameter filters.
        """
        queryset = super().get_queryset()

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")

        queryset = queryset.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        )

        return self._apply_filters(queryset, creator_id, min_price, max_delivery_time)

    def _apply_filters(self, queryset, creator_id, min_price, max_delivery_time):
        """Applies optional query parameter filters."""
        if creator_id:
            queryset = queryset.filter(user=creator_id)

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        return queryset


class OfferdetailSingleView(RetrieveAPIView):
    """
    Returns a single OfferDetail by its ID.
    Primarily referenced via hyperlinks from OfferSerializer.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
