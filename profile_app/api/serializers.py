from rest_framework.serializers import ModelSerializer,CharField

from auth_app.models import UserProfile


class ProfileSerializer(ModelSerializer):
    """
    Serializer for UserProfile including selected User fields.

    Purpose:
    - Returns profile data from `UserProfile`.
    - Exposes selected fields from the related Django `User` model:
        - username (read-only)
        - first_name / last_name (writable, persisted to the User model)

    Note:
    - By using `source="user.<field>"`, User fields are treated as nested data.
      In the `update()` method, these values are explicitly written
      back to `instance.user`.
    """
    username = CharField(source="user.username", read_only=True)
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

    def update(self, instance, validated_data):
        """
        Updates the UserProfile and (optionally) related User fields.

        Workflow:
        1) Extract `user` data from validated_data (if present)
        2) Set and save User attributes
        3) Update remaining UserProfile fields via the ModelSerializer        """
        user_data = validated_data.pop("user", None)
        if user_data:
            self._update_user(instance.user, user_data)

        return super().update(instance, validated_data)

    def _update_user(self, user, user_data):
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()