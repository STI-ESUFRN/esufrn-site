from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from chamado.models import Chamado, Sala
from principal.decorators import allowed_users

chamados_roles = ["suporte"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamado_home(request):
    return render(request, "chamado/dashboard/dashboard.chamado.dashboard.html")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamado_historico(request):
    return render(request, "chamado/dashboard/dashboard.chamado.historico.html")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamado_inserir(request):
    context = {
        "salas": Sala.objects.all(),
    }

    return render(request, "chamado/dashboard/dashboard.chamado.inserir.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamado_relatorio(request):
    chamados = Chamado.objects.select_related("sala").all().order_by("-created")

    status = request.GET.get("status", "")
    requester = (request.GET.get("requester") or "").strip()
    equipment = (request.GET.get("equipment") or "").strip()
    sala = (request.GET.get("sala") or "").strip()
    date_begin = (request.GET.get("date_begin") or "").strip()
    date_end = (request.GET.get("date_end") or "").strip()

    if status:
        chamados = chamados.filter(status=status)

    if requester:
        chamados = chamados.filter(requester__icontains=requester)

    if equipment:
        chamados = chamados.filter(equipment__icontains=equipment)

    if sala == "__other__":
        chamados = chamados.filter(sala__isnull=True).exclude(sala_outros="")
    elif sala:
        chamados = chamados.filter(Q(sala_id=sala) | Q(sala_outros__icontains=sala))

    if date_begin:
        chamados = chamados.filter(date__gte=date_begin)

    if date_end:
        chamados = chamados.filter(date__lte=date_end)

    context = {
        "chamados": chamados,
        "salas": Sala.objects.all(),
        "status_choices": Chamado.Status.choices,
    }

    return render(request, "chamado/dashboard/dashboard.chamado.relatorio.html", context)
