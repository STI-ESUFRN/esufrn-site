from django.urls import path

from dashboard.periodo.views import (
    periodoEditar,
    periodoHistorico,
    periodoHome,
    periodoInserir,
    periodoLista,
)

urlpatterns = [
    path("", periodoHome),
    path("historico/", periodoHistorico, name="periodo_historico"),
    path("inserir/", periodoInserir, name="periodo_inserir"),
    path("lista/", periodoLista, name="periodo_lista"),
    path("editar/<int:pk>/", periodoEditar, name="periodo_editar"),
]
