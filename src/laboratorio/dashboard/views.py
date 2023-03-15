from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from laboratorio.models import Consumable, Permanent
from principal.decorators import allowed_users

material_roles = ["suporte", "material"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def home_view(request):
    return redirect("consumable_dashboard")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def consumable_materials_view(request):
    return render(
        request,
        "laboratorio/dashboard/consumivel/dashboard.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def update_consumable_view(request, pk):
    try:
        item = Consumable.objects.get(id=pk)

    except Consumable.DoesNotExist as err:
        raise Http404(err) from err

    context = {"item": item}
    return render(
        request,
        "laboratorio/dashboard/consumivel/editar.html",
        context,
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_consumable_list_view(request):
    return render(
        request,
        "laboratorio/dashboard/consumivel/relacao.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def permanent_materials_view(request):
    return render(
        request,
        "laboratorio/dashboard/permanente/dashboard.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def update_permanent_view(request, pk):
    try:
        item = Permanent.objects.get(id=pk)

    except Permanent.DoesNotExist as err:
        raise Http404(err) from err

    context = {"item": item}
    return render(
        request,
        "laboratorio/dashboard/permanente/editar.html",
        context,
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_permanent_list_view(request):
    return render(
        request,
        "laboratorio/dashboard/permanente/relacao.html",
    )
