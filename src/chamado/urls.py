from django.urls import include, path

from chamado.views import inserir_chamado

urlpatterns = [
    path("inserir/", inserir_chamado),
    path("tickets/", include("chamado.api.urls")),
]
