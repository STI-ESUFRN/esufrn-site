from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsSafeMethods(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.method in permissions.SAFE_METHODS


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.is_anonymous
