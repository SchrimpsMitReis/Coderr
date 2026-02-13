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
    Registers a new user.

    - Access: Public (AllowAny)
    - Expects: username, email, password, repeated_password, type
    - Creates: User + UserProfile (handled in serializer) and a DRF Token
    - Response (201): token, username, email, user_id
    - Error (400): Serializer validation errors
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new account and returns an authentication token.

        Note:
        - Validation is handled inside RegistrationSerializer
          (including password matching and uniqueness checks).
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response(
            self._build_auth_payload(user, token),
            status=status.HTTP_201_CREATED
        )

    def _build_auth_payload(self, user, token):
        """Builds the standardized authentication response payload."""
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }


class LoginView(APIView):
    """
    Authenticates a user and returns their authentication token.

    - Access: Public (AllowAny)
    - Expects: username, password
    - Response (200): token, username, email, user_id
    - Error (400): Invalid credentials (raised by LoginSerializer)
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validates credentials and returns an authentication token.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            self._build_auth_payload(user, token),
            status=status.HTTP_200_OK
        )

    def _build_auth_payload(self, user, token):
        """Builds the standardized authentication response payload."""
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }