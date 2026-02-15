from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from auth_app.models import UserProfile


class OfferPermission(BasePermission):

    def _profile_type(self, user):
        try:
            return UserProfile.objects.get(user=user).type
        except UserProfile.DoesNotExist:
            return None

    def has_permission(self, request, view):
        if view.action == "list":
            return True

        if view.action == "create":
            return (
                request.user.is_authenticated and
                self._profile_type(request.user) == UserProfile.UserType.BUSINESS
            )

        if view.action == "retrieve":
            return request.user.is_authenticated

        if view.action in ["update", "partial_update", "destroy"]:
            return request.user.is_authenticated

        return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return request.user.is_authenticated

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.user == request.user

        return True
