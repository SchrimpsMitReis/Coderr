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
    queryset = Offer.objects.all()
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    pagination_class = OfferPagination
    search_fields = ['title__icontains', 'description__icontains']
    ordering_fields = [
        "updated_at",
        "min_price",
    ]
    ordering = ['updated_at']

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OfferSerializerPostPatch
        if self.action == "retrieve":
            return OfferSingleSerializer   # falls du da extra Output willst
        return OfferSerializer             # list etc.

    def get_queryset(self):
        queryset = Offer.objects.all()
        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")
        queryset = queryset.annotate(
            min_price=Min("details__price"),
            max_delivery_time=Max("details__delivery_time_in_days"))

        queryset = self._check_filters(queryset,creator_id, min_price,max_delivery_time)
        return queryset

    def _check_filters(self, queryset, creator_id, min_price, max_delivery_time):
        if creator_id:
            queryset = queryset.filter(user=creator_id)

        if min_price:
            queryset = queryset.filter(min_price__gte = min_price)

        if max_delivery_time:
            queryset = queryset.filter(max_delivery_time__lte = max_delivery_time)

        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class OfferdetailSingleView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class= OfferDetailSerializer

