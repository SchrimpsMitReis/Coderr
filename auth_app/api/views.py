from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from auth_app.api.serializers import LoginSerializer, RegistrationSerializer
from auth_app.models import UserProfile
from rest_framework import status


class RegistrationView(APIView):
    """
    Registriert einen neuen Benutzer.

    - Zugriff: öffentlich (AllowAny)
    - Erwartet: username, email, password, repeated_password, type
    - Erstellt: User + UserProfile (im Serializer) und ein DRF Token
    - Antwort (201): token, username, email, user_id
    - Fehler (400): Validierungsfehler des Serializers
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Erstellt einen Account und gibt ein Token zurück.

        Hinweis:
        - Validierung läuft im RegistrationSerializer (inkl. Passwortvergleich
          und Eindeutigkeitschecks).
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response(self._build_auth_payload(user, token), status=status.HTTP_201_CREATED)

    def _build_auth_payload(self, user, token):
        """Formatiert die Standard-Antwort für Auth-Responses."""
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }


class LoginView(APIView):
    """
    Authentifiziert einen Benutzer und gibt sein Token zurück.

    - Zugriff: öffentlich (AllowAny)
    - Erwartet: username, password
    - Antwort (200): token, username, email, user_id
    - Fehler (400): ungültige Credentials (aus LoginSerializer)
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validiert Credentials und gibt das bestehende oder neue Token zurück.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(self._build_auth_payload(user, token), status=status.HTTP_200_OK)

    def _build_auth_payload(self, user, token):
        """Formatiert die Standard-Antwort für Auth-Responses."""
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }