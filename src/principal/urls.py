from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from principal.views import (
    busca,
    email_subscribe,
    email_unsubscribe,
    ensino_especializacao,
    ensino_graduacao,
    ensino_mestrado,
    ensino_pronatec,
    ensino_pronatec_institucional,
    ensino_sobre,
    ensino_tecnico,
    inicio,
    instituicao_documentos,
    instituicao_equipe,
    noticia,
    noticias,
    pagina,
    pronatec_fotos,
    pronatec_videos,
    publicacoes_outras,
)

app_name = "principal"

urlpatterns = [
    path("", inicio, name="home"),
    path("busca/", busca, name="busca"),
    path("ensino/especializacao/", ensino_especializacao, name="ensino_especializacao"),
    path("ensino/graduacao/", ensino_graduacao, name="ensino_graduacao"),
    path("ensino/mestrado/", ensino_mestrado, name="ensino_mestrado"),
    path(
        "ensino/pronatec/institucional",
        ensino_pronatec_institucional,
        name="ensino_pronatec_institucional",
    ),
    path("ensino/pronatec/", ensino_pronatec, name="ensino_pronatec"),
    path("ensino/sobre/", ensino_sobre, name="ensino_sobre"),
    path("ensino/tecnico/", ensino_tecnico, name="ensino_tecnico"),
    path("instituicao/documentos/", instituicao_documentos, name="documentos"),
    path("instituicao/equipe/", instituicao_equipe, name="equipe"),
    path("newsletter/subscribe/", email_subscribe, name="subscribe"),
    path("newsletter/unsubscribe/", email_unsubscribe, name="unsubscribe"),
    path("noticias/", noticias, name="noticias"),
    path("noticias/<slug:slug>/", noticia, name="noticia"),
    path("pagina/<slug:path>/", pagina, name="pagina"),
    path("publicacoes/outras", publicacoes_outras, name="publicacoes_outras"),
    path("pronatec/videos", pronatec_videos, name="pronatec_videos"),
    path("pronatec/fotos/", pronatec_fotos, name="pronatec_fotos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
