from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.helpers import get_dash_context
from principal.decorators import allowed_users

chamados_roles = ["suporte"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamadoHome(request):
    context = {}
    get_dash_context(context, "Chamados", "dashboard")
    return render(request, "chamado/dashboard.chamado.dashboard.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamadoHistorico(request):
    context = {}
    get_dash_context(context, "Chamados", "historico")
    return render(request, "chamado/dashboard.chamado.historico.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=chamados_roles)
def chamadoInserir(request):
    context = {}
    get_dash_context(context, "Chamados", "chamado")
    return render(request, "chamado/dashboard.chamado.inserir.html", context)
