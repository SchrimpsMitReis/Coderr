from rest_framework.serializers import ModelSerializer,CharField

from auth_app.models import UserProfile


class ProfileSerializer(ModelSerializer):
    """
    Serializer für UserProfile inkl. ausgewählter User-Felder.

    Ziel:
    - Liefert Profil-Daten aus `UserProfile`.
    - Mappt bestimmte Felder aus dem verknüpften Django `User`:
        - username (read-only)
        - first_name / last_name (schreibbar, werden auf User gespeichert)

    Hinweis:
    - Durch `source="user.<field>"` werden User-Felder als "nested" Daten behandelt.
      In `update()` schreiben wir diese Werte explizit auf `instance.user`.
    """

    # User.username nur anzeigen (nicht änderbar)
    username = CharField(source="user.username", read_only=True)

    # User.first_name / last_name dürfen über das Profil-Endpoint gepflegt werden
    first_name = CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = CharField(source="user.last_name", required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        # Optional (wenn du es willst): user/created_at typischerweise read-only
        # read_only_fields = ["user", "created_at", "username"]

    def update(self, instance, validated_data):
        """
        Aktualisiert UserProfile und (optional) zugehörige User-Felder.

        Ablauf:
        1) `user`-Daten aus validated_data herausziehen (falls vorhanden)
        2) User-Attribute setzen und speichern
        3) Restliche UserProfile-Felder via ModelSerializer aktualisieren
        """
        user_data = validated_data.pop("user", None)
        if user_data:
            self._update_user(instance.user, user_data)

        return super().update(instance, validated_data)

    def _update_user(self, user, user_data):
        """Schreibt gemappte Felder (z.B. first_name/last_name) auf das User-Objekt."""
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()