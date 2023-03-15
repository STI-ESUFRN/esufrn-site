from django.urls import path

from reserva.dashboard.periodo.views import (
    create_period,
    list_periods,
    period_history,
    periodo_home,
    update_period,
)

urlpatterns = [
    path("", periodo_home, name="periodo_home"),
    path("historico/", period_history, name="period_history"),
    path("inserir/", create_period, name="create_period"),
    path("lista/", list_periods, name="list_periods"),
    path("editar/<int:pk>/", update_period, name="update_period"),
]
