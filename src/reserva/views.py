from django.shortcuts import render

from reserva.models import Classroom


def home_reserva(request):
    salas = Classroom.objects.all()
    context = {
        "salas": salas,
        "crumbs": [{"name": "Informática"}, {"name": "Reserva de Salas"}],
    }

    return render(request, "informatica.reserva.inserir.html", context)
