from rest_framework import permissions

from .models import UserRole

MODERATOR_ALLOWED_ACTIONS = ('PATCH', 'DELETE')


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.admin
            or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == UserRole.moderator)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in MODERATOR_ALLOWED_ACTIONS
            and request.user.role == UserRole.moderator
        )


class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
