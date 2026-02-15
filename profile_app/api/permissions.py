from rest_framework.permissions import BasePermission, SAFE_METHODS

class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # GET/HEAD/OPTIONS erlaubt für jeden Authenticated
        if request.method in SAFE_METHODS:
            return True

        # PATCH/PUT/DELETE nur Besitzer
        if request.method == "PATCH":
            return obj.user == request.user
        
    
