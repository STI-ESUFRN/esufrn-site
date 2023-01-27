from django.urls import path

from dashboard.reserva.views import (
    create_reserve,
    reserve_history,
    reserve_home,
    reserve_report,
)

urlpatterns = [
    path("", reserve_home),
    path("historico/", reserve_history),
    path("inserir/", create_reserve),
    path("relatorio/", reserve_report),
]
