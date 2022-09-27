from django.urls import path

from reserva.views import homeReserva

urlpatterns = [
    path("inserir/", homeReserva),
]
