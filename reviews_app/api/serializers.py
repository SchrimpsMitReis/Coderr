
from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField

from reviews_app.models import Review


class ReviewListSerializer(ModelSerializer):
    """
    Serializer für Reviews (List/Create-geeignet).

    Felder:
    - reviewer ist read-only und wird typischerweise aus `request.user` gesetzt
      (z.B. in perform_create im View oder im Serializer.create()).

    Validierung:
    - Beim Erstellen (instance is None) wird geprüft, ob der aktuelle User
      den gleichen business_user bereits bewertet hat (1 Review pro Kombination).
    """

    reviewer = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        Objektweite Validierung.

        Regel:
        - Ein Reviewer darf einen Business-User nur einmal bewerten.
        - Die Prüfung wird nur beim Create ausgeführt (self.instance is None).
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)

        # Falls kein Request im Context steckt (z.B. Serializer manuell benutzt),
        # keine request-basierte Validierung erzwingen.
        if not request or not user:
            return attrs

        # Create-Fall: nur hier auf Duplicate prüfen
        if self.instance is None:
            business_user = attrs.get("business_user")

            # business_user ist für Create erforderlich
            if business_user is None:
                raise ValidationError({"business_user": ["This field is required."]})

            # Duplicate-Check (ein Review pro reviewer+business_user)
            if Review.objects.filter(reviewer=user, business_user=business_user).exists():
                raise ValidationError(
                    {"non_field_errors": ["Du hast diesen Anbieter bereits bewertet."]}
                )

        return attrs