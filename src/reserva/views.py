

from django.shortcuts import render

from .models import Classroom


def homeReserva(request):
    salas = Classroom.objects.all()
    context = {
        "salas": salas,
        "crumbs": [
            {"name": "Informática"},
            {"name": "Reserva de Salas"}
        ]
    }

    return render(request, "informatica.reserva.inserir.html", context)
