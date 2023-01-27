from django.urls import path

from dashboard.periodo.views import (
    create_period,
    list_periods,
    period_history,
    periodo_home,
    update_period,
)

urlpatterns = [
    path("", periodo_home),
    path("historico/", period_history, name="period_history"),
    path("inserir/", create_period),
    path("lista/", list_periods),
    path("editar/<int:pk>/", update_period),
]
