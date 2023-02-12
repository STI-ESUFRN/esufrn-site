from django.urls import path

from dashboard.chamado.views import chamadoHistorico, chamadoHome, chamadoInserir

urlpatterns = [
    path("", chamadoHome),
    path("historico/", chamadoHistorico),
    path("inserir/", chamadoInserir),
]
