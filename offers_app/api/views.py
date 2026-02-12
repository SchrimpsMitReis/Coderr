from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from offers_app.api.pagination import OfferPagination
from offers_app.models import Offer, OfferDetail
from offers_app.api.serializers import OfferDetailSerializer, OfferSerializer, OfferSerializerPostPatch, OfferSingleSerializer
from rest_framework.generics import RetrieveAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max
from rest_framework.filters import OrderingFilter, SearchFilter

class OfferViewSet(ModelViewSet):
    """
    ViewSet für Offers (CRUD).

    Features:
    - Auth erforderlich (IsAuthenticated)
    - Pagination via OfferPagination
    - Suche über Titel/Beschreibung
    - Ordering (z.B. updated_at, min_price)
    - Query-Parameter-Filter:
        - creator_id: Offers eines bestimmten Users
        - min_price: minimaler Paketpreis >= X
        - max_delivery_time: minimale Lieferzeit <= X
    """

    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]

    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    # SearchFilter erwartet Feldnamen (Lookups macht DRF intern)
    search_fields = ["title", "description"]

    ordering_fields = ["updated_at", "min_price"]
    ordering = ["updated_at"]

    def get_serializer_class(self):
        """
        Wählt je nach Action den passenden Serializer.
        - create/update/partial_update: Nested input (Details)
        - retrieve: detaillierter Output
        - list: kompakter Output mit Aggregationen
        """
        if self.action in ["create", "update", "partial_update"]:
            return OfferSerializerPostPatch
        if self.action == "retrieve":
            return OfferSingleSerializer
        return OfferSerializer

    def get_queryset(self):
        """
        Annotiert Aggregationen für Filtering/Ordering und wendet Query-Param-Filter an.
        """
        queryset = super().get_queryset()

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")

        # Aggregationen DB-seitig (für Ordering/Filtering)
        queryset = queryset.annotate(
            min_price=Min("details__price"),
            min_delivery_time=Min("details__delivery_time_in_days"),
        )

        return self._apply_filters(queryset, creator_id, min_price, max_delivery_time)

    def _apply_filters(self, queryset, creator_id, min_price, max_delivery_time):
        """Wendet optionale Query-Parameter-Filter an."""
        if creator_id:
            queryset = queryset.filter(user=creator_id)

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        return queryset
    
class OfferdetailSingleView(RetrieveAPIView):
    """
    Liefert ein einzelnes OfferDetail anhand der ID.
    Wird v.a. über Hyperlinks aus OfferSerializer referenziert.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer