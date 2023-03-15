from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    return render(request, "chamado/dashboard/dashboard.chamado.inserir.html")
