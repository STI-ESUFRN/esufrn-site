from django.urls import path

from reserva.views import cancel_reserve, home_reserva

urlpatterns = [
    path("inserir/", home_reserva),
    path("cancelar/<uuid:uuid>", cancel_reserve, name="cancel_reserve"),
]
