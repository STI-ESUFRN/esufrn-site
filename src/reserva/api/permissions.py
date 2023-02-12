from rest_framework import permissions


class IsFromReserve(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="reserva").exists()


class IsFromCoordination(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="cordenacao").exists()


class IsFromDirection(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="direcao").exists()
