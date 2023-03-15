from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min
from django.shortcuts import redirect, render
from django.utils import timezone

from principal.decorators import allowed_users
from reserva.models import Classroom, Period

periodo_roles = ["reserva", "suporte", "coordenacao"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def periodo_home(request):
    return redirect("period_history")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def create_period(request):
    salas = Classroom.objects.all()
    cursos = Period.Course.choices
    context = {"salas": salas, "cursos": cursos}
    return render(
        request, "reserva/dashboard/periodo/dashboard.periodo.inserir.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def period_history(request):
    context = {
        "cursos": Period.Course.choices,
        "salas": Classroom.objects.all(),
    }
    return render(
        request, "reserva/dashboard/periodo/dashboard.periodo.historico.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def list_periods(request):
    period = request.GET.get("period") or timezone.now().year

    base = Period.objects.filter(period__icontains=period)

    if course := request.GET.get("course"):
        base = base.filter(course=course)

    if class_period := request.GET.get("class_period"):
        base = base.filter(class_period=class_period)

    period_groups = []
    groups = base.values("course", "period", "class_period").annotate(Count("id"))
    for group in groups:
        periods = Period.objects.filter(
            course=group["course"],
            period=group["period"],
            class_period=group["class_period"],
        )
        date_begin = (
            periods.values("date_begin")
            .annotate(Min("date_begin"))
            .order_by("date_begin")[0]["date_begin__min"]
        )

        period_groups.append(
            {
                "course": Period.Course(group["course"]).label,
                "period": group["period"],
                "class_period": group["class_period"],
                "date_begin": date_begin,
                "periods": periods,
            }
        )

    reservas = Period.objects.all()
    turmas = (
        reservas.order_by("class_period")
        .values_list("class_period", flat=True)
        .distinct()
    )
    periodos = reservas.order_by("period").values_list("period", flat=True).distinct()
    courses = Period.Course.choices

    context = {
        "period_groups": period_groups,
        "cursos": courses,
        "turmas": turmas,
        "periodos": periodos,
    }

    return render(
        request, "reserva/dashboard/periodo/dashboard.periodo.lista.html", context
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def update_period(request, pk):
    period = Period.objects.get(id=pk)
    salas = Classroom.objects.all()
    cursos = Period.Course.choices
    context = {
        "period": period,
        "salas": salas,
        "cursos": cursos,
    }
    return render(
        request, "reserva/dashboard/periodo/dashboard.periodo.editar.html", context
    )
