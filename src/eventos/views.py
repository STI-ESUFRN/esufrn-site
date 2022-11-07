from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

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
    events = Event.available_objects.filter(
        date_begin__gte=datetime.now().date(), date_end__lte=datetime.now().date()
    )

    page = int(request.GET.get("page", "1"))
    result_obj, qnt, intervalo = paginator(page, events)

    context = {
        "events": events,
        "crumbs": [
            {"name": "Eventos"},
            {"name": "Em andamento"},
        ],
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
