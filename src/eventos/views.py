from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from eventos.models import Event


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
