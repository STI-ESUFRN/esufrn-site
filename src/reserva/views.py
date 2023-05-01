from django.http import Http404
from django.shortcuts import render

from dashboard.helpers import get_current_reserves
from reserva.enums import Status
from reserva.models import Classroom, Reserve


def home_reserva(request):
    salas = Classroom.objects.filter(public=True)
    context = {
        "salas": salas,
        "crumbs": [
            {"name": "Reserva de Salas"},
            {"name": "Inserir reserva"},
        ],
    }

    return render(request, "informatica.reserva.inserir.html", context)


def cancel_reserve(request, uuid):
    try:
        reserve = Reserve.objects.exclude(status=Status.CANCELED).get(uuid=uuid)

    except Reserve.DoesNotExist as e:
        raise Http404 from e

    reserve.status = Status.CANCELED
    reserve.save()

    context = {
        "crumbs": [
            {"name": "Reserva de Salas"},
            {"name": "Cancelar reserva"},
        ],
    }
    return render(request, "informatica.reserva.cancelar.html", context)


def calendar_view(request):
    queryset = get_current_reserves()
    events = queryset.filter(reserve__isnull=False)
    classes = queryset.filter(period__isnull=False)
    context = {
        "crumbs": [
            {"name": "Reserva de Salas"},
            {"name": "Calendário"},
        ],
        "events": events,
        "classes": classes,
    }
    return render(request, "informatica.reserva.calendario.html", context)
