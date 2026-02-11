from rest_framework import serializers
from rest_framework import status

from auth_app.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from auth_app.models import UserProfile

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    repeated_password = serializers.CharField(required=True, write_only=True)
    type = serializers.ChoiceField(required=True, choices=UserProfile.UserType.choices)  # falls du TextChoices nutzt

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({"repeated_password": "passwords dont match"})
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "already exists"})
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "already exists"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        UserProfile.objects.create(
            user=user,
            email=validated_data["email"],
            type=validated_data.get("type", UserProfile.UserType.CUSTOMER),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials"})
        attrs["user"] = user
        return attrs