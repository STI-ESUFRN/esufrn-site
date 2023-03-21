from django.urls import include, path

from api.views import ContatosView, ContatoView, search

urlpatterns = [
    path("busca/", search, name="search"),
    path("contato/", ContatosView.as_view()),
    path("contato/<int:pk>/", ContatoView.as_view()),
    path("", include("chamado.api.urls")),
    path("", include("laboratorio.api.urls")),
    path("", include("reserva.api.urls")),
]
