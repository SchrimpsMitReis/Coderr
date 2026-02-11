from django.db.models import Q
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from auth_app.models import UserProfile


class OrdersPermission(BasePermission):
    """
    Regeln:
    - Customer: darf POST (create)
    - Business: darf PATCH/PUT nur, wenn er business_user der Order ist
    - GET (retrieve): Customer oder Business nur, wenn beteiligt (customer_user oder business_user)
    - DELETE: nur staff/admin
    """

    def _profile_type(self, user):
        try:
            return UserProfile.objects.get(user=user).type
        except UserProfile.DoesNotExist:
            return None

    def _is_profile_type_legal(self, user, view):
        ptype = self._profile_type(user)

        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        if view.action == "create":
            return ptype == UserProfile.UserType.CUSTOMER

        if view.action in ["update", "partial_update"]:
            return ptype == UserProfile.UserType.BUSINESS
        
        return True
    
    def _is_profile_type_legal(self, user, view):
        ptype = self._profile_type(user)

        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        if view.action == "create":
            return ptype == UserProfile.UserType.CUSTOMER

        if view.action in ["update", "partial_update"]:
            return ptype == UserProfile.UserType.BUSINESS

        return True

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        ptype = self._profile_type(user)

        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        if view.action == "create":
            return ptype == UserProfile.UserType.CUSTOMER

        if view.action in ["update", "partial_update"]:
            return ptype == UserProfile.UserType.BUSINESS

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # DELETE nur staff/admin (zur Sicherheit auch hier)
        if view.action == "destroy":
            return user.is_staff or user.is_superuser

        # GET retrieve: nur wenn beteiligt
        if view.action == "retrieve":
            return (obj.customer_user_id == user.id) or (obj.business_user_id == user.id)

        # PATCH/PUT: nur Seller (business_user) und nur eigene Order
        if view.action in ["update", "partial_update"]:
            return obj.business_user_id == user.id

        return True