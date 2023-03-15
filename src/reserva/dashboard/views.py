from django.shortcuts import redirect


def dashboard_reserve_view(request):
    return redirect("reserve_home")
