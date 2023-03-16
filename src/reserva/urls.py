from django.urls import path

from reserva.views import calendar_view, cancel_reserve, home_reserva

urlpatterns = [
    path("inserir/", home_reserva),
    path("calendario/", calendar_view),
    path("cancelar/<uuid:uuid>", cancel_reserve, name="cancel_reserve"),
]
