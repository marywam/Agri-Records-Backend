from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow only Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsFarmer(BasePermission):
    """Allow only Farmer users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "farmer"


class IsOwnerOrAdmin(BasePermission):
    """Farmers can only access their own crops. Admins can access all."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        # IMPORTANT: use obj.farmer, not obj.user
        return obj.farmer == request.user

