from rest_framework.permissions import BasePermission, SAFE_METHODS

# class IsOwnerOrAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return obj.user == request.user or request.user.is_staff
#         return request.user.is_staff  # Only admin can update/delete

from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit, but allow read-only access to all.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff