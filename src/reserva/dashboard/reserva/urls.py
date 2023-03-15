from django.urls import path

from reserva.dashboard.reserva.views import (
    create_reserve,
    reserve_history,
    reserve_home,
    reserve_report,
)

urlpatterns = [
    path("", reserve_home, name="reserve_home"),
    path("historico/", reserve_history, name="reserve_history"),
    path("inserir/", create_reserve, name="create_reserve"),
    path("relatorio/", reserve_report, name="reserve_report"),
]
