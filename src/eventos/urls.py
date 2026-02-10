from django.urls import path

from eventos.views import evento, eventos, eventos_concluidos, submissao_trabalhos, submeter_trabalho, inscricao, submeter_inscricao

urlpatterns = [
    path("", eventos, name="eventos"),
    path("concluido/", eventos_concluidos, name="eventos_concluidos"),
    path("submissao/", submissao_trabalhos, name="submissao_trabalhos"),
    path("submissao/submeter/", submeter_trabalho, name="submeter_trabalho"),
    path("inscricao/", inscricao, name="inscricao"),
    path("inscricao/submeter/", submeter_inscricao, name="submeter_inscricao"),
    path("<slug:slug>/", evento, name="evento"),
]
