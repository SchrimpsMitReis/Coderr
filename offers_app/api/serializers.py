
from django.contrib.auth.models import User

from rest_framework import serializers
from auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for OfferDetail.

    Usage:
    - Embedding OfferDetails during create/update (POST/PATCH).
    - Detailed representation of the three packages (basic/standard/premium).
    """

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferDetailHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Lightweight serializer for OfferDetail references.

    Usage:
    - Used in offer list responses to reference details via hyperlinks
      instead of embedding full detail data.
    """

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the offer list view.

    Includes:
    - Core offer data
    - Hyperlinks to offer details
    - Aggregations across details (min_price, min_delivery_time)
    - Selected user data (user_details) for UI display
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """Calculates the minimum price across all OfferDetails."""
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """Calculates the minimum delivery time across all OfferDetails."""
        delivery_time = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None

    def get_user_details(self, obj):
        """
        Returns selected user information.

        Note:
        - For full profile data, using UserProfile would often be preferable.
          Here, only basic User fields are returned.
        """
        user = obj.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferSerializerPostPatch(serializers.ModelSerializer):
    """
    Serializer for creating and updating Offers (POST/PATCH).

    Rules:
    - `user` is automatically set from the request (HiddenField / CurrentUserDefault).
    - On POST, exactly 3 OfferDetails must be submitted
      (one each for basic, standard, premium).
    - Only BUSINESS profiles may create or modify offers (validate_user).
    - Create operation creates Offer + details (via bulk_create).
    - Update modifies Offer and optionally updates details by offer_type.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "details"]

    def validate(self, data):
        """
        Object-level validation.

        Sets `image` to an empty string if None is provided,
        ensuring consistent database values.
        """
        image = data.get("image")
        if image is None:
            data["image"] = ""
        return data

    def validate_details(self, value):
        """
        Validates the details list.

        On POST:
        - Exactly 3 details must be provided.
        - offer_type must contain exactly: basic, standard, premium (one each).
        """
        request = self.context.get("request")

        if request and request.method == "POST":
            if len(value) != 3:
                raise serializers.ValidationError("Exactly 3 OfferDetails must be provided.")

            types = [d["offer_type"] for d in value]
            if sorted(types) != ["basic", "premium", "standard"]:
                raise serializers.ValidationError(
                    "offer_type must contain exactly: basic, standard, premium (one each)."
                )

        return value

    def validate_user(self, attrs):
        """
        Ensures only BUSINESS users may create or modify offers.

        Note:
        - Validation is intentionally based on UserProfile,
          not on user.is_staff or similar flags.
        """
        user = self.context["request"].user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("UserProfile not found.")

        if profile.type != UserProfile.UserType.BUSINESS:
            raise serializers.ValidationError({"permission": "business_required"})

        return attrs

    def create(self, validated_data):
        """
        Creates Offer and associated OfferDetails.

        Performance:
        - OfferDetails are created using bulk_create.
        """
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **d) for d in details_data]
        )
        return offer

    def update(self, instance, validated_data):
        """
        Updates Offer and optionally its details.

        - Offer fields are updated via the ModelSerializer.
        - Details are updated only if provided in the request.
        """
        details = validated_data.pop("details", None)
        instance = super().update(instance, validated_data)

        if details is not None:
            self._update_details(instance, details)

        return instance

    def _update_details(self, instance, details):
        """
        Updates OfferDetails based on their offer_type.

        Expectations:
        - Each detail object in the payload must include offer_type.
        - The existing detail with the matching offer_type is updated.
        """
        for d in details:
            offer_type = d.get("offer_type")
            if not offer_type:
                raise serializers.ValidationError(
                    {"details": "offer_type is required for updating a detail."}
                )

            try:
                detail_obj = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"No OfferDetail with offer_type='{offer_type}' found for this offer."}
                )

            for field, value in d.items():
                if field != "offer_type":
                    setattr(detail_obj, field, value)

            detail_obj.save()


class OfferSingleSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single Offer.

    Includes:
    - Core offer data
    - Hyperlinks to OfferDetails
    - Aggregated values (min_price, min_delivery_time)
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "details",
            "min_price",
            "min_delivery_time",
            "created_at",
            "updated_at"
        ]

    def get_min_price(self, obj):
        """Calculates the minimum price across all OfferDetails."""
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """Calculates the minimum delivery time across all OfferDetails."""
        delivery_time = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None

class OfferFilterSerializer(serializers.Serializer):
    max_delivery_time = serializers.IntegerField(required=False, min_value=0)
    min_price = serializers.IntegerField(required=False, min_value=0)
    search = serializers.CharField(required=False, allow_blank=True)
    page_size = serializers.IntegerField(required=False, min_value=1)