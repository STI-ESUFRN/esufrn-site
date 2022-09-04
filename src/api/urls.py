from django.urls import include, path

from .views import *

urlpatterns = [
    path('busca/', search, name='search'),
    path('contato', contatosView.as_view()),
    path('contato/<int:pk>', contatoView.as_view()),

    # API DE RESERVA DE SALAS
    path("", include("reserva.api.urls")),

    # API DE CHAMADOS
    path("", include("chamado.api.urls")),

    # API DE INVENTÁRIO
    path("", include("inventario.api.urls")),
]
