from rest_framework import permissions


class GroupAlmoxarifado(permissions.BasePermission):
    def has_permission(self, request, _):
        return (
            request.user.groups.filter(name="almoxarifado") or request.user.is_superuser
        )
