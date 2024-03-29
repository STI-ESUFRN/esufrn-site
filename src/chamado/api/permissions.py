from rest_framework import permissions


class GroupSuporte(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.groups.filter(name="suporte") or request.user.is_superuser
