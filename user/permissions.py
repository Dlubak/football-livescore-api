from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners/admins
    of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_superuser
