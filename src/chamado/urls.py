from django.urls import path

from chamado.views import inserirChamado

urlpatterns = [
    path("inserir", inserirChamado),
]
