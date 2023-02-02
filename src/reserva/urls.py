from django.urls import path

from reserva.views import home_reserva

urlpatterns = [
    path("inserir/", home_reserva),
]
