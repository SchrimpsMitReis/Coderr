from rest_framework import serializers
from rest_framework import status

from auth_app.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.

    Responsibilities:
    - Validates registration data (username, email, password).
    - Ensures both password fields match.
    - Verifies username and email uniqueness.
    - Creates a new User and the corresponding UserProfile.

    Note:
    - `repeated_password` is used only for validation
      and is not stored in the database.
    """

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    repeated_password = serializers.CharField(required=True, write_only=True)
    type = serializers.ChoiceField(
        required=True,
        choices=UserProfile.UserType.choices
    )

    # Validation

    def validate(self, attrs):
        """Orchestrates object-level registration validation."""
        self._validate_passwords_match(attrs)
        self._validate_username_unique(attrs["username"])
        self._validate_email_unique(attrs["email"])
        return attrs

    def _validate_passwords_match(self, attrs):
        """Ensures the password and repeated password are identical."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )

    def _validate_username_unique(self, username):
        """Ensures the username is not already in use."""
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Already exists."})

    def _validate_email_unique(self, email):
        """Ensures the email address is not already in use."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Already exists."})

    # Creation

    def create(self, validated_data):
        """
        Creates the User and corresponding UserProfile.
        `repeated_password` is removed before persistence.
        """
        validated_data.pop("repeated_password")
        user = self._create_user(validated_data)
        self._create_profile(user, validated_data)
        return user

    def _create_user(self, data):
        """Creates the Django User instance (with password hashing)."""
        return User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )

    def _create_profile(self, user, data):
        """Creates or updates the associated UserProfile."""
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "email": data["email"],
                "type": data.get("type", UserProfile.UserType.CUSTOMER),
            },
        )

        profile.email = data["email"]
        profile.type = data.get("type", UserProfile.UserType.CUSTOMER)
        profile.save()

class LoginSerializer(serializers.Serializer):
    """
    Validates login credentials using Django's `authenticate`.

    Result:
    - On success, the authenticated User instance
      is stored in `attrs["user"]`.
    - Token generation is typically handled in the view.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticates the user credentials."""
        user = self._authenticate(attrs["username"], attrs["password"])
        attrs["user"] = user
        return attrs

    def _authenticate(self, username, password):
        """Performs authentication and raises an error if invalid."""
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )
        return user