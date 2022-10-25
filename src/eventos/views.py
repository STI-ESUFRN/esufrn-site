from django.http import Http404
from django.shortcuts import render

from eventos.models import Event


def eventos(request):
    events = Event.available_objects.all()
    context = {
        "events": events,
    }

    return render(request, "eventos.eventos.html", context)


def evento(request, pk):
    event = Event.available_objects.filter(id=pk)
    if not event:
        raise Http404()

    context = {
        "event": event,
    }

    return render(request, "eventos.evento.html", context)
