from django.urls import include, path

urlpatterns = [
    path("periodo/", include("reserva.dashboard.periodo.urls")),
    path("reserva/", include("reserva.dashboard.reserva.urls")),
]
