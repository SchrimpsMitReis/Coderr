from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders

class OrderSerializer(serializers.ModelSerializer):
    """
    Read serializer for Orders.

    Purpose:
    - Returns the complete Order representation for list/retrieve endpoints.
    - Used as response serializer after order creation.
    - All fields are read-only because Orders represent a snapshot
      of OfferDetail data and must not be modified by the client
      (exception: status via OrderUpdateSerializer).
    """

    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Orders
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields

    def get_updated_at(self, obj):

        if obj.updated_at and obj.created_at == obj.updated_at:
            return ""
        

        if obj.updated_at:
            return obj.updated_at.isoformat().replace("+00:00", "Z")

        return ""


class OrderUpdateSerializer(OrderSerializer):
    """
    Update serializer for Orders.

    Purpose:
    - Allows updating only the order status
      (e.g., from in_progress → completed).
    - All other fields remain read-only and are inherited
      from the parent serializer.
    """

    status = serializers.ChoiceField(
        choices=Orders.StatusType.choices,
        required=True
    )

    class Meta(OrderSerializer.Meta):

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
        ]


class OrderCreateSerializer(OrderSerializer):
    """
    Create serializer for Orders.

    Input:
    - offer_detail_id (write-only):
        References the selected OfferDetail (basic/standard/premium).

    Behavior:
    - Creates an Order as a snapshot of the referenced OfferDetail.
    - Copies title, price, delivery time, features, and offer_type.
    - Sets the initial status to IN_PROGRESS.
    - customer_user is derived from request.user.
    - business_user is derived from the Offer owner.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ["offer_detail_id"]

    def create(self, validated_data):
        """
        Creates an Order based on the referenced OfferDetail.

        Notes:
        - 'offer_detail_id' is removed from validated_data
          because it is not a model field.
        - get_object_or_404 returns HTTP 404 if the ID is invalid.
        """
        request = self.context["request"]

        offer_detail = get_object_or_404(
            OfferDetail,
            id=validated_data.pop("offer_detail_id"),
        )

        return Orders.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status=Orders.StatusType.IN_PROGRESS,
        )


class OrderCountSerializer(serializers.ModelSerializer):
    """
    Generic serializer (e.g., useful for debugging or statistics).

    Clean Code Note:
    - If you truly want all model fields, use:
        fields = "__all__"
      not:
        ['__all__']
    """

    class Meta:
        model = Orders
        fields = "__all__"