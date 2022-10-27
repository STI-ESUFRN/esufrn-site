from django.urls import path

from principal.views import (
    busca,
    email_subscribe,
    email_unsubscribe,
    ensino_especializacao,
    ensino_graduacao,
    ensino_mestrado,
    ensino_pronatec,
    ensino_sobre,
    ensino_tecnico,
    inicio,
    instituicao_documentos,
    instituicao_equipe,
    noticia,
    noticias,
    pagina,
    publicacoes_outras,
)

urlpatterns = [
    path("", inicio, name="home"),
    path("pagina/<slug:path>/", pagina, name="pagina"),
    path("instituicao/equipe/", instituicao_equipe),
    path("instituicao/documentos/", instituicao_documentos),
    path("ensino/sobre/", ensino_sobre, name="ensino_sobre"),
    path("ensino/tecnico/", ensino_tecnico, name="ensino_tecnico"),
    path("ensino/graduacao/", ensino_graduacao, name="ensino_graduacao"),
    path("ensino/especializacao/", ensino_especializacao, name="ensino_especializacao"),
    path("ensino/mestrado/", ensino_mestrado, name="ensino_mestrado"),
    path("ensino/pronatec/", ensino_pronatec, name="ensino_pronatec"),
    path("publicacoes/outras", publicacoes_outras, name="publicacoes_outras"),
    path("busca/", busca, name="busca"),
    path("noticias/<slug:slug>/", noticia, name="noticia"),
    path("noticias/", noticias, name="noticias"),
    path("newsletter/unsubscribe", email_unsubscribe, name="unsubscribe"),
    path("newsletter/subscribe", email_subscribe, name="subscribe"),
]
