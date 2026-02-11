from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Orders
        fields = ["id", "customer_user", "business_user","title", "revisions", "delivery_time_in_days","price", "features", "offer_type","status", "created_at",]
        read_only_fields = ["id", "customer_user", "business_user","title", "revisions", "delivery_time_in_days","price", "features", "offer_type","status", "created_at"]


class OrderUpdateSerializer(OrderSerializer):
    status = serializers.ChoiceField(choices=Orders.StatusType.choices, required=True)

    class Meta(OrderSerializer.Meta):
        read_only_fields = [
            "id", "customer_user", "business_user",
            "title", "revisions", "delivery_time_in_days",
            "price", "features", "offer_type", "created_at",
        ]  


class OrderCreateSerializer(OrderSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ["offer_detail_id"]


    def create(self, validated_data):
        request = self.context["request"]
        offer_detail = get_object_or_404(OfferDetail, id=validated_data.pop("offer_detail_id"))
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

    # business_user_id =

    class Meta:
        model = Orders
        fields = ['__all__']
