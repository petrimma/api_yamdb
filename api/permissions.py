from rest_framework import permissions

from .models import User

MODERATOR_ALLOWED_ACTIONS = ('update', 'destroy')


class ReadOnly(permissions.BasePermission):
    """Provide ReadOnly access to list and detail"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """the permission provides full access for admin users and superusers"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == User.UserRole.ADMIN
                or request.user.is_superuser)


class IsAuthorOrModerator(permissions.BasePermission):
    """The permission provides actions to update and destroy if user is author
     or moderator of the site"""

    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                and request.user.role == User.UserRole.USER
                or request.user.is_authenticated
                and request.user.role == User.UserRole.MODERATOR
                and view.action in MODERATOR_ALLOWED_ACTIONS)
