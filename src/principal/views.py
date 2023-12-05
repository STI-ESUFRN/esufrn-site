import json
import os
import threading
import unicodedata
from datetime import timedelta
from functools import reduce

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from principal.forms import NewsletterForm
from principal.helpers import email_token, join_range, paginator, qnt_page
from principal.models import (
    Alert,
    Document,
    News,
    Newsletter,
    Page,
    Photo,
    Team,
    Testimonial,
    Links_V,
    destaque,
    Noticia,
)


def pagina(request, path):
    try:
        page = Page.objects.get(path=path)
        context = {"status": "success", "page": page, "crumbs": [{"name": page.name}]}

        return render(request, "home.pagina.html", context)

    except Exception as e:
        raise Http404 from e


def inicio(request):
    newsletter = NewsletterForm()

    settings.BOLD = ""
    # pegando os valores para o template
    now = timezone.now()
    queryset = News.objects.filter(published=True)
    post = queryset.filter(
        Q(category="noticia") | Q(category="processo") | Q(category="concurso"),
    ).filter(published_at__lt=now)[:3]

    post_events = (
        queryset.filter(category="evento")
        .filter(published_at__gt=now)
        .order_by("published_at")[:3]
    )
    important = queryset.filter(is_important=True)[:4]
    depoimentos = Testimonial.objects.all()

    alertas = Alert.objects.filter(expires_at__gt=timezone.now())

    context = {
        "post": post,
        "events": post_events,
        "important": important,
        "depoimentos": depoimentos,
        "newsletter": newsletter,
        "alertas": alertas,
    }

    return render(request, "home.principal.html", context)


# ---------------------------------------------------------------------


def noticias(request):
    news = News.objects.all()

    category = request.GET.get("category")
    if category:
        news = news.filter(category=category)

    period = request.GET.get("period")
    if period:
        if period == "hora":
            delta = timedelta(hours=1)
        elif period == "dia":
            delta = timedelta(days=1)
        elif period == "semana":
            delta = timedelta(weeks=1)
        elif period == "mes":
            delta = relativedelta(months=+1)
        elif period == "ano":
            delta = relativedelta(years=+1)
        else:
            delta = timedelta()

        now = timezone.now()
        news = news.filter(published_at__range=(now - delta, now))

    page = int(request.GET.get("page", "1"))

    result_obj, qnt, intervalo = paginator(page, news)

    context = {
        "news": result_obj,
        "pag": page,
        "status": "success",
        "total": qnt,
        "rng": intervalo,
        "crumbs": [{"name": "Notícias"}],
    }

    return render(request, "home.noticias.html", context)


def noticia(request, slug):
    try:
        news = News.objects.get(slug=slug)

    except News.DoesNotExist as exc:
        raise Http404 from exc

    context = {
        "status": "success",
        "news": news,
        "crumbs": [
            {"name": "Notícias", "link": reverse("principal:noticias")},
            {"name": news.title},
        ],
    }

    return render(request, "home.noticia.html", context)


def instituicao_equipe(request):
    equipe = Team.objects.all()
    context = {"equipe": equipe, "crumbs": [{"name": "Insituição"}, {"name": "Equipe"}]}

    return render(request, "instituicao.equipe.html", context)


# ---------------------------------------------------------------------


def ensino_sobre(request):
    settings.BOLD = ""

    context = {"crumbs": [{"name": "Ensino"}, {"name": "Sobre"}]}
    return render(request, "ensino.sobre.html", context)


def ensino_tecnico(request):
    settings.BOLD = ""

    context = {
        "curso": "tecnico",
        "crumbs": [{"name": "Ensino"}, {"name": "Técnico e Pós-Técnico"}],
    }
    return render(request, "ensino.tecnico.html", context)


def ensino_graduacao(request):
    settings.BOLD = ""

    context = {
        "curso": "graduacao",
        "crumbs": [{"name": "Ensino"}, {"name": "Graduação Tecnológica"}],
    }
    return render(request, "ensino.tecnico.html", context)


def ensino_especializacao(request):
    settings.BOLD = ""

    context = {
        "curso": "especializacao",
        "crumbs": [{"name": "Ensino"}, {"name": "Especialização Lato Senso"}],
    }
    return render(request, "ensino.tecnico.html", context)


def ensino_mestrado(request):
    settings.BOLD = ""

    return redirect(
        "https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=10489",
    )


def ensino_pronatec_institucional(request):
    settings.BOLD = ""
    context = {
        "curso": "pronatec",
        "crumbs": [{"name": "Ensino"}, {"name": "Pronatec"}],
    }
    return render(request, "ensino.tecnico.html", context)

# ---------------------------------------------------------------------


def email_unsubscribe(request):
    crumbs = [
        {"name": "Newsletter"},
        {"name": "Cancelar subscrição"},
    ]
    settings.BOLD = ""

    email = request.GET.get("email")
    token = request.GET.get("token")
    if email and token:
        _token = email_token(email)
        if _token == token:
            result = Newsletter.objects.filter(email__iexact=email)
            if result:
                result.delete()
                threading.Thread(
                    target=send_mail,
                    args=(
                        (
                            "Newsletter ESUFRN",
                            "Seu email foi descadastrado de nossa Newsletter.",
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                    ),
                ).start()

                context = {
                    "status": "success",
                    "message": "Email descadastrado",
                    "crumbs": crumbs,
                }
                return render(request, "email.unsubscribe.html", context)

    context = {
        "status": "error",
        "message": "Ocorreu um erro ao descadastrar o email",
        "crumbs": crumbs,
    }
    return render(request, "email.unsubscribe.html", context)


@require_POST
def email_subscribe(request):
    try:
        name_person = request.POST.get("name_person")
        email = request.POST.get("email")
        consent = request.POST.get("consent") == "on"
        category = str(request.POST.get("category")).split(",")

        newsletter = Newsletter.objects.filter(email__iexact=email)
        if newsletter:
            newsletter.update(
                name_person=name_person,
                category=category,
                consent=consent,
            )
            return JsonResponse(
                {"status": "success", "message": "Cadastro atualizado com sucesso"},
            )

        Newsletter.objects.create(
            name_person=name_person,
            email=email,
            category=category,
            consent=consent,
        )
        return JsonResponse(
            {"status": "success", "message": "Email cadastrado com sucesso"},
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": "{}".format(next(iter(e)))})


# ---------------------------------------------------------------------


def busca(request):
    crumbs = [
        {"name": "Notícias", "link": reverse("principal:noticias")},
        {"name": "Resultados da busca"},
    ]
    news = News.objects.all()

    if category := request.GET.get("category"):
        news = news.filter(category=category)

    if period := request.GET.get("period"):
        if period == "hora":
            delta = timedelta(hours=1)
        elif period == "dia":
            delta = timedelta(days=1)
        elif period == "semana":
            delta = timedelta(weeks=1)
        elif period == "mes":
            delta = relativedelta(months=+1)
        elif period == "ano":
            delta = relativedelta(years=+1)
        else:
            delta = timedelta()

        now = timezone.now()
        news = news.filter(published_at__range=(now - delta, now))

    page = int(request.GET.get("page", "1"))

    result_obj_blog = []
    result_obj_pub = []
    result_cur = []
    total_intervalo = range(0, 0)

    total_qnt = 0
    if field_search := request.GET.get("termo"):
        settings.BOLD = field_search
        words = field_search.split()

        # BUSCA PELAS NOTÍCIAS
        if not category or (category != "curso" and category != "publicacao"):
            result_blog = news.filter(
                reduce(
                    lambda x, y: x & y,
                    [
                        (
                            Q(title__icontains=word)
                            | Q(subtitle__icontains=word)
                            | Q(news__icontains=word)
                            | Q(category__icontains=word)
                        )
                        for word in words
                    ],
                ),
            ).order_by("-modified")

            result_obj_blog, qnt, intervalo = paginator(page, result_blog)

            total_qnt = qnt
            total_intervalo = join_range(intervalo, intervalo, total_qnt)

        # BUSCA PELOS ARQUIVOS JSON
        if not category or category == "curso":

            def read_json(file):
                result = []
                with open(os.path.join(settings.STATIC_ROOT, file)) as json_file:
                    data = json.load(json_file)

                for line in data:
                    for word in words:
                        if unicodedata.normalize("NFKD", word.lower()).encode(
                            "ASCII",
                            "ignore",
                        ) in unicodedata.normalize("NFKD", line["nome"].lower()).encode(
                            "ASCII",
                            "ignore",
                        ):
                            result.append(line)
                            break

                return result

            courses = []
            courses += read_json("assets/json/ensino.tecnico.json")
            courses += read_json("assets/json/ensino.especializacao.json")
            courses += read_json("assets/json/ensino.graduacao.json")
            courses += read_json("assets/json/ensino.postecnico.json")
            courses += read_json("assets/json/ensino.pronatec.json")

            result_cur, qnt, intervalo = paginator(page, courses)
            total_qnt = qnt_page(total_qnt, qnt)
            total_intervalo = join_range(total_intervalo, intervalo, total_qnt)

        context = {
            "news": result_obj_blog,
            "result_pub": result_obj_pub,
            "result_cur": result_cur,
            "pag": page,
            "category": category if category else None,
            "period": period if period else None,
            "search": field_search,
            "status": "success",
            "total": total_qnt,
            "rng": total_intervalo,
            "crumbs": crumbs,
        }

    else:
        context = {
            "status": "error",
            "mensagem": "error",
            "crumbs": crumbs,
        }

    return render(request, "home.busca.html", context)


def instituicao_documentos(request):
    categories = (
        ("institucional", "Institucional"),
        ("ensino", "Ensino"),
    )
    list = []
    queryset = Document.objects.exclude(is_active=False)
    for index, category in categories:
        docs = queryset.filter(category=index)
        list.append({"main": category, "documentos": docs})

    context = {
        "categorias": list,
        "crumbs": [{"name": "Instituição"}, {"name": "Documentos"}],
    }

    return render(request, "instituicao.documentos.html", context)


def publicacoes_outras(request):
    anos_list = (
        Document.objects.filter(category="publicacoes")
        .order_by("-date__year")
        .values_list("date__year", flat=True)
        .distinct()
    )

    anos = []
    for ano in anos_list:
        publicacoes = Document.objects.filter(category="publicacoes", date__year=ano)
        anos.append(
            {
                "ano": ano if ano is not None else "Não Especificado",
                "publicacoes": publicacoes,
            },
        )

    context = {
        "anos": anos,
        "crumbs": [{"name": "Publicações"}, {"name": "Outras publicações"}],
    }
    return render(request, "publicacoes.outraspublicacoes.html", context)


def pronatec_fotos(request):  # Recupere todas as fotos do banco de dados
    photos = Photo.objects.all()

    context = {"photos": photos}

    return render(request, "pronatec_fotos.html", context)


def pronatec_videos(request):
    links = Links_V.objects.all()

    context = {"links": links}

    return render(request, "pronatec_videos.html", context)
# ---------------------------------------------------------------------
def ensino_pronatec(request):
    # Recupere todas as fotos e vídeos do banco de dados
    photos = Photo.objects.all()
    links = Links_V.objects.all()

    # Recupere todos os destaques
    destaques = destaque.objects.all()
    noticias = Noticia.objects.all()
    context = {
        "curso": "pronatec",
        "crumbs": [{"name": "Ensino"}, {"name": "Pronatec"}],
        "photos": photos,
        "links": links,
        "destaques": destaques,
        "noticias": noticias,
    }

    return render(request, "ensino.pronatec.html", context)