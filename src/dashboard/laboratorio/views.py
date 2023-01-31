from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from dashboard.helpers import get_dash_context
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
    context = {}
    get_dash_context(context, "Laboratorio", "consumable_dashboard")
    return render(
        request, "laboratorio/dashboard.laboratorio.consumivel.dashboard.html", context
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
        request, "laboratorio/dashboard.laboratorio.consumivel.editar.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_consumable_list_view(request):
    context = {}
    get_dash_context(context, "Laboratorio", "relacao")
    return render(
        request, "laboratorio/dashboard.laboratorio.consumivel.relacao.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def permanent_materials_view(request):
    context = {}
    get_dash_context(context, "Laboratorio", "permanent_dashboard")
    return render(
        request, "laboratorio/dashboard.laboratorio.permanente.dashboard.html", context
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
        request, "laboratorio/dashboard.laboratorio.permanente.editar.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_permanent_list_view(request):
    context = {}
    get_dash_context(context, "Laboratorio", "relacao")
    return render(
        request, "laboratorio/dashboard.laboratorio.permanente.relacao.html", context
    )
