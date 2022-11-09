from django.urls import path

from eventos.views import evento, eventos, eventos_concluidos

urlpatterns = [
    path("", eventos, name="eventos"),
    path("concluido/", eventos_concluidos, name="eventos_concluidos"),
    path("<slug:slug>/", evento, name="evento"),
]
