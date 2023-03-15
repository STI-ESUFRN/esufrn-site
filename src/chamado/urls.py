from django.urls import include, path

from chamado.views import inserirChamado

urlpatterns = [
    path("inserir/", inserirChamado),
    path("tickets/", include("chamado.api.urls")),
]
