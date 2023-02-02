from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.helpers import get_dash_context
from principal.decorators import allowed_users
from reserva.models import Classroom, UserClassroom

reserva_roles = ["reserva", "suporte"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=reserva_roles)
def reserve_home(request):
    context = {}
    get_dash_context(context, "Reservas", "reserva_dashboard")
    return render(request, "reserva/dashboard.reserva.dashboard.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=reserva_roles)
def reserve_history(request):
    if request.user.is_superuser:
        salas = Classroom.objects.all()

    else:
        user_classroomns = UserClassroom.objects.filter(user=request.user).values_list(
            "classroom", flat=True
        )
        salas = Classroom.objects.filter(id__in=user_classroomns)

    context = {"salas": salas}
    get_dash_context(context, "Reservas", "reserva_historico")
    return render(request, "reserva/dashboard.reserva.historico.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=reserva_roles)
def create_reserve(request):
    if request.user.is_superuser:
        salas = Classroom.objects.all()

    else:
        user_classroomns = UserClassroom.objects.filter(user=request.user).values_list(
            "classroom", flat=True
        )
        salas = Classroom.objects.filter(id__in=user_classroomns)

    context = {"salas": salas}
    get_dash_context(context, "Reservas", "inserir_reserva")
    return render(request, "reserva/dashboard.reserva.inserir.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=reserva_roles)
def reserve_report(request):
    salas = Classroom.objects.all()
    classroom_id = request.GET.get("classroom")
    sala = None
    if classroom_id is not None:
        sala = Classroom.objects.get(id=classroom_id)

    context = {
        "salas": salas,
        "sala": sala,
    }
    get_dash_context(context, "Reservas", "relatorio")
    return render(request, "reserva/dashboard.reserva.relatorio.html", context)
