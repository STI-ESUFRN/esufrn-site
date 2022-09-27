from rest_framework import permissions


class IsUserFromSupport(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.groups.filter(name="suporte")


class IsUserFromCoordination(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.groups.filter(name="coordenacao")


class IsUserFromReserve(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.groups.filter(name="reserva")
