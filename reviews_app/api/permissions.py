from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from auth_app.models import UserProfile
from reviews_app.models import Review


class ReviewPermission(BasePermission):
    """
    Regeln:
    - LIST/RETRIEVE: nur authenticated
    - CREATE (POST): nur customer
    - PATCH/PUT: nur customer, dem der Review gehört (reviewer)
    - DELETE: nur customer, dem der Review gehört (reviewer)
    """

    message = "Keine Berechtigung für diese Aktion."

    def _is_customer(self, user) -> bool:
        try:
            return UserProfile.objects.get(user=user).type == UserProfile.UserType.CUSTOMER
        except UserProfile.DoesNotExist:
            return False

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if view.action in ["list", "retrieve"]:
            return True

        if view.action == "create":
            return self._is_customer(user)

        if view.action in ["update", "partial_update", "destroy"]:
            return self._is_customer(user)

        return False

    def has_object_permission(self, request, view, obj: Review):
        user = request.user

        if view.action == "retrieve":
            return True

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.reviewer_id == user.id

        return True