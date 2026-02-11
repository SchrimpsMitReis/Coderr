from rest_framework import serializers
from rest_framework import status

from auth_app.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer für die Benutzerregistrierung.

    Verantwortlichkeiten:
    - Validiert Registrierungsdaten (Username, E-Mail, Passwort).
    - Prüft, ob Passwörter übereinstimmen.
    - Stellt sicher, dass Username und E-Mail eindeutig sind.
    - Erstellt einen neuen User sowie das zugehörige UserProfile.

    Hinweis:
    - `repeated_password` dient ausschließlich der Validierung
      und wird nicht gespeichert.
    """

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    repeated_password = serializers.CharField(required=True, write_only=True)
    type = serializers.ChoiceField(
        required=True,
        choices=UserProfile.UserType.choices
    )

    # Validate

    def validate(self, attrs):
        """Orchestriert die Registrierung-Validierung (objektweit)."""
        self._validate_passwords_match(attrs)
        self._validate_username_unique(attrs["username"])
        self._validate_email_unique(attrs["email"])
        return attrs

    def _validate_passwords_match(self, attrs):
        """Stellt sicher, dass Passwort und Wiederholung identisch sind."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({"repeated_password": "passwords dont match"})

    def _validate_username_unique(self, username):
        """Stellt sicher, dass der Username noch nicht vergeben ist."""
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "already exists"})

    def _validate_email_unique(self, email):
        """Stellt sicher, dass die E-Mail noch nicht vergeben ist."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "already exists"})

    # Method / Action

    def create(self, validated_data):
        """Erstellt User + UserProfile. `repeated_password` wird nicht gespeichert."""
        validated_data.pop("repeated_password")
        user = self._create_user(validated_data)
        self._create_profile(user, validated_data)
        return user

    def _create_user(self, data):
        """Erstellt den Django User (inkl. Passwort-Hashing via `create_user`)."""
        return User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )

    def _create_profile(self, user, data):
        """Erstellt das zugehörige UserProfile."""
        UserProfile.objects.create(
            user=user,
            email=data["email"],
            type=data.get("type", UserProfile.UserType.CUSTOMER),
        )
    


class LoginSerializer(serializers.Serializer):
    """
    Validiert Login-Credentials über Django `authenticate`.

    Ergebnis:
    - Bei Erfolg wird das User-Objekt in `attrs["user"]` abgelegt.
    - Token-Erstellung erfolgt typischerweise in der View.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authentifiziert den User und hängt ihn an die validierten Daten."""
        user = self._authenticate(attrs["username"], attrs["password"])
        attrs["user"] = user
        return attrs

    def _authenticate(self, username, password):
        """Wrapper um `authenticate` mit klarer Fehlermeldung."""
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials"})
        return user


