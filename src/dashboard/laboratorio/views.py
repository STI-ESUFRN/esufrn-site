from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from dashboard.helpers import get_dash_context
from laboratorio.models import Consumable, Material, Permanent
from principal.decorators import allowed_users

material_roles = ["suporte", "material"]


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
def create_consumable_material_view(request):
    context = {}
    get_dash_context(context, "Laboratorio", "inserir_consumivel")
    return render(
        request, "laboratorio/dashboard.laboratorio.consumivel.inserir.html", context
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
def create_permanent_material_view(request):
    context = {}
    get_dash_context(context, "Laboratorio", "inserir_permanente")
    return render(
        request, "laboratorio/dashboard.laboratorio.permanente.inserir.html", context
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
def materials_list_view(request):
    materials = Material.objects.all()
    context = {"materials": materials}
    get_dash_context(context, "Laboratorio", "relacao")
    return render(request, "laboratorio/dashboard.laboratorio.relacao.html", context)
