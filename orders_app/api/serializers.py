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
    Read-Serializer für Orders.

    Zweck:
    - Liefert eine vollständige Order-Darstellung für List/Retrieve/Response nach Create.
    - Alle Felder sind read-only, da Orders aus OfferDetails "gesnapshottet" werden und
      nicht frei vom Client geändert werden sollen (Ausnahme: Status via Update-Serializer).
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
        ]
        # Gleiche Liste wie fields -> übersichtlich und eindeutig read-only
        read_only_fields = fields


class OrderUpdateSerializer(OrderSerializer):
    """
    Update-Serializer für Orders.

    Zweck:
    - Erlaubt ausschließlich das Aktualisieren des Status (z.B. in_progress -> completed).
    - Alle anderen Felder bleiben read-only und werden vom Parent-Serializer geerbt.
    """

    status = serializers.ChoiceField(choices=Orders.StatusType.choices, required=True)

    class Meta(OrderSerializer.Meta):
        # status ist hier bewusst NICHT read-only
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
    Create-Serializer für Orders.

    Input:
    - offer_detail_id (write-only): Referenz auf das gewünschte OfferDetail (basic/standard/premium)

    Verhalten:
    - Erstellt eine Order als Snapshot der OfferDetail-Daten (Titel, Preis, Lieferzeit, Features, offer_type).
    - Setzt den Status initial auf IN_PROGRESS.
    - `customer_user` wird aus request.user übernommen, `business_user` aus dem OfferDetail-Angebot.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta(OrderSerializer.Meta):
        # Output bleibt wie OrderSerializer; zusätzlich wird offer_detail_id als Input akzeptiert
        fields = OrderSerializer.Meta.fields + ["offer_detail_id"]

    def create(self, validated_data):
        """
        Erzeugt die Order aus dem referenzierten OfferDetail.

        Hinweis:
        - offer_detail_id wird aus validated_data entfernt, da es kein Model-Feld ist.
        - get_object_or_404 liefert 404, wenn offer_detail_id ungültig ist.
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
    Allgemeiner Serializer (z.B. für Debug/Stats).

    Clean-Code-Hinweis:
    - Wenn du wirklich alle Felder willst, nutze fields = "__all__" (string),
      nicht ['__all__'] (liste).
    """

    class Meta:
        model = Orders
        fields = "__all__"

