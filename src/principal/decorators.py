from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def unauthenticated_user(redirect_to="/"):
    def decorator(view):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view(request, *args, **kwargs)

        return wrapper_func

    return decorator


def authenticated_user(redirect_to="/"):
    def decorator(view):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_to)
            return view(request, *args, **kwargs)

        return wrapper_func

    return decorator


def allowed_users(allowed_roles=list):
    def decorator(view):
        def wrapper_func(request, *args, **kwargs):
            if (
                request.user.groups.filter(name__in=allowed_roles)
                or request.user.is_superuser
            ):
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper_func

    return decorator
