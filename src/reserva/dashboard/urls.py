from django.urls import include, path

from reserva.dashboard.views import dashboard_reserve_view

urlpatterns = [
    path("periodo/", include("reserva.dashboard.periodo.urls")),
    path("reserva/", include("reserva.dashboard.reserva.urls")),
    path("", dashboard_reserve_view),
]
