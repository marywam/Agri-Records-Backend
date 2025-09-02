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
    """Farmers can only access their own crops or profile. Admins can access all."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        # Farmers can only see their own profile or crops
        if hasattr(obj, "farmer"):  # Crop model
            return obj.farmer == request.user
        return obj == request.user  # User model (profile)


