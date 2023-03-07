from django.urls import path

from chamado.dashboard.views import chamado_historico, chamado_home, chamado_inserir

urlpatterns = [
    path("", chamado_home),
    path("historico/", chamado_historico),
    path("inserir/", chamado_inserir),
]
