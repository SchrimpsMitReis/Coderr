from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from auth_app.models import UserProfile


class OrdersPermission(BasePermission):
    """
    Custom permission class controlling access to Order endpoints.

    Rules:
    - Customer:
        - May create orders (POST).
    - Business:
        - May update orders (PATCH/PUT) only if they are the assigned business_user.
    - Retrieve (GET single object):
        - Allowed only if the user is involved in the order
          (either customer_user or business_user).
    - Delete:
        - Restricted to staff or superuser only.
    """

    def _profile_type(self, user):
        """
        Returns the UserProfile type of the given user.

        Returns:
        - UserProfile.UserType value
        - None if no profile exists
        """
        try:
            return UserProfile.objects.get(user=user).type
        except UserProfile.DoesNotExist:
            return None

    def has_permission(self, request, view):
        """
        View-level permission check (before accessing a specific object).

        Determines whether the user is allowed to perform the requested action
        in general (e.g., create or update).
        """
        user = request.user

        if not user or not user.is_authenticated:
            return False

        profile_type = self._profile_type(user)

        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        if view.action == "create":
            return profile_type == UserProfile.UserType.CUSTOMER

        return True

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.

        Ensures the user is allowed to interact with the specific Order instance.
        """
        user = request.user

        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        if view.action == "retrieve":
            return (
                obj.customer_user_id == user.id
                or obj.business_user_id == user.id
            )

        if view.action in ["update", "partial_update"]:
            return obj.business_user_id == user.id

        return True