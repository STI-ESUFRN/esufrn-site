from rest_framework import permissions


class IsCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"
