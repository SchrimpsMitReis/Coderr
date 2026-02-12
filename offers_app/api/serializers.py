
from django.contrib.auth.models import User

from rest_framework import serializers
from auth_app.models import UserProfile
from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Vollständiger Serializer für OfferDetail.

    Verwendung:
    - Einbetten der OfferDetails bei Create/Update (POST/PATCH).
    - Detaillierte Darstellung der drei Pakete (basic/standard/premium).
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
    Lightweight Serializer für OfferDetail-Referenzen.

    Verwendung:
    - In Offer-Listen, um Details nicht voll zu embedd-en, sondern als Links.
    """

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer für Offer-Listenansicht.

    Enthält:
    - Offer-Stammdaten
    - Hyperlinks zu den Details
    - Aggregationen über Details (min_price, min_delivery_time)
    - Ausgewählte User-Daten (user_details) für die UI
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
        """Berechnet den Minimalpreis über alle OfferDetails."""
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """Berechnet die minimale Lieferzeit über alle OfferDetails."""
        delivery_time = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None

    def get_user_details(self, obj):
        """
        Gibt ausgewählte User-Infos zurück.

        Hinweis:
        - Für echte Profile-Daten wäre oft `UserProfile` sinnvoller,
          hier werden aber Basisdaten des Users geliefert.
        """
        user = obj.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }


class OfferSerializerPostPatch(serializers.ModelSerializer):
    """
    Serializer für Create/Update von Offers (POST/PATCH).

    Regeln:
    - `user` wird aus dem Request gesetzt (HiddenField / CurrentUserDefault).
    - Bei POST müssen genau 3 OfferDetails gesendet werden
      (basic, standard, premium jeweils genau 1x).
    - Nur BUSINESS-Profile dürfen Offers erstellen/ändern (validate_user).
    - Create erstellt Offer + Details (bulk_create).
    - Update aktualisiert Offer und optional Details per offer_type.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "details"]

    def validate(self, data):
        """
        Objektweite Validierung.

        Setzt `image` auf leeren String, wenn None übergeben wurde,
        um konsistente DB-Werte zu behalten.
        """
        image = data.get("image")
        if image is None:
            data["image"] = ""
        return data

    def validate_details(self, value):
        """
        Validiert die Details-Liste.

        Bei POST:
        - exakt 3 Details
        - offer_type enthält genau: basic, standard, premium (je 1x)
        """
        request = self.context.get("request")

        if request and request.method == "POST":
            if len(value) != 3:
                raise serializers.ValidationError("Es müssen genau 3 OfferDetails gesendet werden.")

            types = [d["offer_type"] for d in value]
            if sorted(types) != ["basic", "premium", "standard"]:
                raise serializers.ValidationError(
                    "offer_type muss genau: basic, standard, premium enthalten (je 1x)."
                )

        return value

    def validate_user(self, attrs):
        """
        Stellt sicher, dass nur BUSINESS-User Offers erstellen/ändern.

        Hinweis:
        - Hier wird bewusst über UserProfile geprüft, nicht über user.is_staff o.ä.
        """
        user = self.context["request"].user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("UserProfile not found")

        if profile.type != UserProfile.UserType.BUSINESS:
            raise serializers.ValidationError({"permission": "business_required"})

        return attrs

    def create(self, validated_data):
        """
        Erstellt Offer + OfferDetails.

        Performance:
        - Details werden per bulk_create erzeugt.
        """
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(**validated_data)

        OfferDetail.objects.bulk_create([OfferDetail(offer=offer, **d) for d in details_data])
        return offer

    def update(self, instance, validated_data):
        """
        Aktualisiert Offer und optional Details.

        - Offer-Felder werden über ModelSerializer-Update gesetzt.
        - Details werden nur aktualisiert, wenn sie im Request vorhanden sind.
        """
        details = validated_data.pop("details", None)
        instance = super().update(instance, validated_data)

        if details is not None:
            self._update_details(instance, details)

        return instance

    def _update_details(self, instance, details):
        """
        Aktualisiert OfferDetails anhand ihres offer_type.

        Erwartung:
        - Jedes Detail-Objekt im Payload enthält offer_type.
        - Es wird das existierende Detail mit gleichem offer_type aktualisiert.
        """
        for d in details:
            offer_type = d.get("offer_type")
            if not offer_type:
                raise serializers.ValidationError({"details": "offer_type is required for updating a detail."})

            try:
                detail_obj = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"No OfferDetail with offer_type='{offer_type}' for this offer."}
                )

            for field, value in d.items():
                if field != "offer_type":
                    setattr(detail_obj, field, value)

            detail_obj.save()


class OfferSingleSerializer(serializers.ModelSerializer):
    """
    Serializer für die Detailansicht einer Offer.

    Enthält:
    - Offer-Stammdaten
    - Links zu OfferDetails
    - Aggregationen (min_price, min_delivery_time)
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailHyperlinkedSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "details", "min_price", "min_delivery_time"]

    def get_min_price(self, obj):
        """Berechnet den Minimalpreis über alle OfferDetails."""
        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """Berechnet die minimale Lieferzeit über alle OfferDetails."""
        delivery_time = obj.details.values_list("delivery_time_in_days", flat=True)
        return min(delivery_time) if delivery_time else None