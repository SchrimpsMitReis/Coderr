from rest_framework.permissions import BasePermission


class ProfilePermission(BasePermission):

    def has_permission(self, request, view):
        # Alles braucht Auth
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Nur Besitzer darf verändern
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.user == request.user

        # retrieve erlaubt für jeden authenticated
        if view.action == "retrieve":
            return True

        return True