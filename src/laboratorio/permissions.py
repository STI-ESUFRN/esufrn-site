from rest_framework import permissions


class GroupLaboratorio(permissions.BasePermission):
    def has_permission(self, request, _):
        return (
            request.user.groups.filter(name="laboratorio") or request.user.is_superuser
        )
