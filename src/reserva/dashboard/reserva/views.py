from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from principal.decorators import allowed_users
from reserva.models import Classroom, UserClassroom

reserva_roles = ["reserva", "suporte"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=reserva_roles)
def reserve_home(request):
    return render(request, "reserva/dashboard/reserva/dashboard.reserva.dashboard.html")


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
    return render(
        request, "reserva/dashboard/reserva/dashboard.reserva.historico.html", context
    )


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
    return render(
        request, "reserva/dashboard/reserva/dashboard.reserva.inserir.html", context
    )


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
    return render(
        request, "reserva/dashboard/reserva/dashboard.reserva.relatorio.html", context
    )
