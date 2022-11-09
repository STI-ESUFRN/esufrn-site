from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from eventos.models import Event
from principal.helpers import paginator


def evento(request, slug):
    try:
        event = Event.available_objects.get(slug=slug)

        context = {
            "event": event,
            "crumbs": [
                {"name": "Eventos"},
                {"name": event.name},
            ],
        }

        return render(request, "eventos.evento.html", context)

    except ObjectDoesNotExist:
        raise Http404()


def eventos(request):
    today = datetime.now().date()

    events = Event.available_objects.all()

    category = request.GET.get("category")
    if category == "concluido":
        events = events.filter(date_end__lt=today)
    elif category == "andamento":
        events = events.filter(date_begin__lte=today, date_end__gte=today)
    elif category == "agendado":
        events = events.filter(date_begin__gt=today)

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
        events = events.filter(created__range=(now - delta, now))

    page = int(request.GET.get("page", "1"))
    result_obj, qnt, intervalo = paginator(page, events)

    context = {
        "events": events,
        "crumbs": [
            {"name": "Eventos"},
        ],
        "categories": {
            "parameter": "category=",
            "options": [
                {
                    "verbose_name": "Tudo",
                    "verbose_name_plural": "Tudo",
                    "query": "",
                },
                {
                    "verbose_name": "Concluído",
                    "verbose_name_plural": "Concluídos",
                    "query": "concluido",
                },
                {
                    "verbose_name": "Em andamento",
                    "verbose_name_plural": "Em andamento",
                    "query": "andamento",
                },
                {
                    "verbose_name": "Agendado",
                    "verbose_name_plural": "Agendados",
                    "query": "agendado",
                },
            ],
        },
        "result_obj": result_obj,
        "qnt": qnt,
        "intervalo": intervalo,
    }

    return render(request, "eventos.eventos.html", context)


def eventos_concluidos(request):
    events = Event.available_objects.filter(date_end__lt=datetime.now().date())

    page = int(request.GET.get("page", "1"))
    result_obj, qnt, intervalo = paginator(page, events)

    context = {
        "events": events,
        "crumbs": [
            {"name": "Eventos"},
            {"name": "Concluído"},
        ],
        "result_obj": result_obj,
        "qnt": qnt,
        "intervalo": intervalo,
    }

    return render(request, "eventos.eventos.html", context)
