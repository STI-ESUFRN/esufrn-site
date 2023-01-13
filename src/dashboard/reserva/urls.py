from django.urls import path

from dashboard.reserva.views import (
    reservaHistorico,
    reservaHome,
    reservaInserir,
    reservaRelatorio,
)

urlpatterns = [
    path("", reservaHome),
    path("historico/", reservaHistorico),
    path("inserir/", reservaInserir),
    path("relatorio/", reservaRelatorio),
]
