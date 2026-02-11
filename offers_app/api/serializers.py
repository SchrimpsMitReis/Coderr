
from django.contrib.auth.models import User

from rest_framework import serializers
from auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at",
                  "details", "min_price", "min_delivery_time", 'user_details']

    def get_min_price(self, obj):
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        delivery_time = obj.details.values_list(
            "delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None
    
    def get_user_details(self, obj):
        user = obj.user
        return {
            "first_name" : user.first_name,
            "last_name" :user.last_name,
            "username" :user.username
        }

class OfferSerializerPostPatch(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "details"]

    def validate(self, data):

        image = data.get('image')
        if image == None:
            data["image"] = ""
            return data

    def validate_details(self, value):
        request = self.context.get("request")

        if request and request.method == "POST":
            if len(value) != 3:
                raise serializers.ValidationError(
                    "Es müssen genau 3 OfferDetails gesendet werden.")

            types = [d["offer_type"] for d in value]

            if sorted(types) != ["basic", "premium", "standard"]:
                raise serializers.ValidationError(
                    "offer_type muss genau: basic, standard, premium enthalten (je 1x).")
        return value

    def validate_user(self, attrs):
        user = self.context["request"].user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("UserProfile not found")

        if profile.type != UserProfile.UserType.BUSINESS:
            raise serializers.ValidationError({
                "permission": "business_required"
            })
        return attrs
    
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **d) for d in details_data]
        )

        return offer

    def update(self, instance, validated_data):
        details = validated_data.pop("details", None)
        instance = super().update(instance, validated_data)

        if details is not None:
            self._update_details(instance,details)
        
        return instance

    def _update_details(self, instance, details):
        for d in details:
            offer_type = d.get("offer_type")
            if not offer_type:
                raise serializers.ValidationError({"details": "offer_type is required for updating a detail."})
            
            try:
                detail_obj = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError({"details": f"No OfferDetail with offer_type='{offer_type}' for this offer."})

            for field, value in d.items():
                if field != "offer_type":
                    setattr(detail_obj, field, value)
            detail_obj.save()

class OfferSingleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description",
                  "details", "min_price", "min_delivery_time"]

    def get_min_price(self, obj):
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        delivery_time = obj.details.values_list(
            "delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None

