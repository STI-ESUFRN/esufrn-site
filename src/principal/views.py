import calendar
import json
import os
import threading
import unicodedata
from datetime import date, timedelta, datetime
from functools import reduce

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import models
from django.db.models import Count, Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .middleware import BOT_UA_PATTERNS

from principal.forms import NewsletterForm
from principal.helpers import email_token, join_range, paginator, qnt_page
from principal.models import (
    Alert,
    Cursos_Pronatec,
    Document,
    destaque,
    Links_V,
    News,
    Newsletter,
    Noticia,
    Page,
    PageView,
    Photo,
    Team,
    Testimonial,
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

    # Filtro por intervalo de datas específico (tem precedência sobre 'period')
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if start_date_str or end_date_str:
        # Recarrega queryset básico respeitando categoria
        news = News.objects.all()
        if category:
            news = news.filter(category=category)
        try:
            start_dt = None
            end_dt = None
            if start_date_str:
                # Espera formato YYYY-MM-DD (input type=date)
                start_dt = timezone.make_aware(
                    datetime.strptime(start_date_str, "%Y-%m-%d")
                )
            if end_date_str:
                # Final do dia
                end_raw = datetime.strptime(end_date_str, "%Y-%m-%d")
                end_dt = timezone.make_aware(end_raw) + timedelta(days=1)
            filter_kwargs = {}
            if start_dt and end_dt:
                filter_kwargs["published_at__range"] = (start_dt, end_dt)
            elif start_dt:
                filter_kwargs["published_at__gte"] = start_dt
            elif end_dt:
                filter_kwargs["published_at__lte"] = end_dt
            if filter_kwargs:
                news = news.filter(**filter_kwargs)
        except Exception:
            # Silencia erros de parsing e mantém queryset atual
            pass

    page = int(request.GET.get("page", "1"))

    result_obj, qnt, intervalo = paginator(page, news)

    context = {
        "news": result_obj,
        "pag": page,
        "status": "success",
        "total": qnt,
        "rng": intervalo,
        "crumbs": [{"name": "Notícias"}],
        "start_date": start_date_str if (start_date_str) else "",
        "end_date": end_date_str if (end_date_str) else "",
    }

    return render(request, "home.noticias.html", context)


def noticia(request, slug):
    try:
        news = News.objects.get(slug=slug)
    except News.DoesNotExist as exc:
        raise Http404 from exc

    # --- detecção de bot ---
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_bot = any(pat in ua for pat in BOT_UA_PATTERNS)

    # --- lógica de sessão unificada, só se NÃO for bot ---
    if not is_bot:
        viewed = request.session.get('viewed_news', [])
        if news.id not in viewed:
            tipo = (
                'processo'
                if news.category == News.Category.PROCESS.value
                else 'noticia'
            )
            PageView.objects.create(page_type=tipo, object_id=news.id)

            # incrementa contador no próprio objeto News
            # Atualiza o contador diretamente via QuerySet update para evitar
            # chamar o método save() do modelo (que atualizaria campos como
            # `modified` por causa de TimeStampedModel). Usando update() não
            # dispara lógica adicional nem altera o campo `modified`.
            News.objects.filter(pk=news.pk).update(views=models.F('views') + 1)
            news.refresh_from_db()

            viewed.append(news.id)
            request.session['viewed_news'] = viewed

    # --- renderiza normalmente ---
    pageview_count = PageView.objects.filter(
        object_id=news.id,
        page_type__in=['noticia', 'processo']
    ).count()

    return render(
        request,
        "home.noticia.html",
        {
            "status": "success",
            "news": news,
            "crumbs": [
                {"name": "Notícias", "link": reverse("principal:noticias")},
                {"name": news.title},
            ],
            "pageview_count": pageview_count,
        }
    )


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

    # Filtro rápido por período relativo
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

    # Filtro por intervalo de datas específico (tem precedência sobre 'period')
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    if start_date_str or end_date_str:
        # Ignora filtro de período relativo anterior se intervalo explícito for usado
        # Recarrega queryset básico respeitando categoria
        news = News.objects.all()
        if category := request.GET.get("category"):
            news = news.filter(category=category)
        try:
            start_dt = None
            end_dt = None
            if start_date_str:
                # Espera formato YYYY-MM-DD (input type=date)
                start_dt = timezone.make_aware(
                    datetime.strptime(start_date_str, "%Y-%m-%d")
                )
            if end_date_str:
                # Final do dia
                end_raw = datetime.strptime(end_date_str, "%Y-%m-%d")
                end_dt = timezone.make_aware(end_raw) + timedelta(days=1)
            filter_kwargs = {}
            if start_dt and end_dt:
                filter_kwargs["published_at__range"] = (start_dt, end_dt)
            elif start_dt:
                filter_kwargs["published_at__gte"] = start_dt
            elif end_dt:
                filter_kwargs["published_at__lte"] = end_dt
            if filter_kwargs:
                news = news.filter(**filter_kwargs)
        except Exception:
            # Silencia erros de parsing e mantém queryset atual
            pass

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
            ).order_by("-published_at")

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
            "start_date": start_date_str if (start_date_str) else "",
            "end_date": end_date_str if (end_date_str) else "",
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
            "start_date": request.GET.get("start_date", ""),
            "end_date": request.GET.get("end_date", ""),
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

def instituicao_projetos(request):
    categories = (
        ("institucional", "Institucional"),
        ("ensino", "Ensino"),
    )
    list = []
    queryset = Document.objects.exclude(is_active=False)
    for index, category in categories:
        docs = queryset.filter(category=index)
        documentos = []
        
        for doc in docs:
            documentos.append({
                "name": doc.name,
                "document_type": doc.document_type,
                "file": doc.file.url if doc.document_type == "arquivo" else None,
                "link": doc.link if doc.document_type == "link" else None,
                "ensino_subcategory": doc.ensino_subcategory
            })
        list.append({"main": category, "documentos": docs})

    context = {
        "categorias": list,
        "crumbs": [{"name": "Instituição"}, {"name": "Projetos"}],
    }

    return render(request, "instituicao.projetos.html", context)

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
    noticias = Noticia.objects.all().order_by('-data_criacao')
    cursos = Cursos_Pronatec.objects.all()
    context = {
        "curso": "pronatec",
        "crumbs": [{"name": "Ensino"}, {"name": "Pronatec"}],
        "photos": photos,
        "links": links,
        "destaques": destaques,
        "noticias": noticias,
        "cursos": cursos,
    }

    return render(request, "ensino.pronatec.html", context)


def Cusos_pronatec(request):
    cursos = Cursos_Pronatec.objects.all()
    context = {"cursos": cursos}

    return render(request, 'Cursos_pronatec.html', {'cursos': cursos})

@login_required
def dashboard_metrics(request):
    # --- parâmetros de filtro via GET (podem estar vazios) ---
    year = request.GET.get('year')       # ex.: '2025' ou None
    month = request.GET.get('month')     # ex.: '4' ou None
    week = request.GET.get('week')       # ex.: '1' ou None

    # queryset base (todos os registros)
    queryset = PageView.objects.all()

    # filtra por ano, se fornecido
    if year:
        year = int(year)
        queryset = queryset.filter(timestamp__year=year)

    # filtra por mês, se fornecido
    if month:
        month = int(month)
        queryset = queryset.filter(timestamp__month=month)

    # filtra por semana, apenas se year+month+week estiverem
    if year and month and week:
        week = int(week)
        _, days_in_month = calendar.monthrange(year, month)
        start_day = (week - 1) * 7 + 1
        end_day = min(week * 7, days_in_month)
        start_date = date(year, month, start_day)
        end_date   = date(year, month, end_day)
        queryset = queryset.filter(timestamp__date__range=(start_date, end_date))

    # --- métricas ---
    site_views      = queryset.filter(page_type='site')
    total_site      = site_views.count()
    total_news      = queryset.filter(page_type='noticia').count()
    total_processos = queryset.filter(page_type='processo').count()

    # Top 5 notícias e processos
    top_news_qs = (
        queryset.filter(page_type='noticia')
        .values('object_id')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )
    top_proc_qs = (
        queryset.filter(page_type='processo')
        .values('object_id')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # mapeia títulos
    news_map = {
        n.id: n.title
        for n in News.objects.filter(id__in=[x['object_id'] for x in top_news_qs])
    }
    proc_map = {
        n.id: n.title
        for n in News.objects.filter(id__in=[x['object_id'] for x in top_proc_qs])
    }

    # --- contexto p/ template ---
    context = {
        # filtros
        'selected_year':  year,
        'selected_month': month,
        'selected_week':  week,
        'years':  list(range(2025, timezone.now().year + 1)),
        'months': list(range(1, 13)),
        'weeks':  [1, 2, 3, 4, 5],

        # métricas
        'total_site':      total_site,
        'total_news':      total_news,
        'total_processos': total_processos,
        'top_news':        [(news_map[x['object_id']], x['total']) for x in top_news_qs],
        'top_processos':   [(proc_map[x['object_id']], x['total']) for x in top_proc_qs],
    }
    return render(request, 'dashboard_metrics.html', context)