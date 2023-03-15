from django.urls import include, path

from api.views import contatosView, contatoView, search

urlpatterns = [
    path("busca/", search, name="search"),
    path("contato/", contatosView.as_view()),
    path("contato/<int:pk>/", contatoView.as_view()),
    path("", include("chamado.api.urls")),
    path("", include("laboratorio.api.urls")),
    path("", include("reserva.api.urls")),
]
