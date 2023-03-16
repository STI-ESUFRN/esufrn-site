from django.http import Http404
from django.shortcuts import render

from reserva.enums import Status
from reserva.models import Classroom, Reserve


def home_reserva(request):
    salas = Classroom.objects.all()
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
        raise Http404(e)

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
    context = {
        "crumbs": [
            {"name": "Reserva de Salas"},
            {"name": "Calendário"},
        ],
    }
    return render(request, "informatica.reserva.calendario.html", context)
