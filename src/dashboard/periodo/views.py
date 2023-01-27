from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min
from django.shortcuts import redirect, render

from dashboard.helpers import get_dash_context
from principal.decorators import allowed_users
from reserva.models import Classroom, PeriodReserve

periodo_roles = ["reserva", "suporte", "coordenacao"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def periodo_home(request):
    return redirect("period_history")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def create_period(request):
    salas = Classroom.objects.all()
    cursos = PeriodReserve.get_courses()
    context = {"salas": salas, "cursos": cursos}
    get_dash_context(context, "Períodos", "inserir_periodo")
    return render(request, "periodo/dashboard.periodo.inserir.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def period_history(request):
    reservas = PeriodReserve.objects.all()

    professores = (
        reservas.order_by("requester").values_list("requester", flat=True).distinct()
    )
    idsalas = (
        reservas.order_by("classroom").values_list("classroom", flat=True).distinct()
    )
    turmas = (
        reservas.order_by("class_period")
        .values_list("class_period", flat=True)
        .distinct()
    )
    periodos = reservas.order_by("period").values_list("period", flat=True).distinct()

    courses = PeriodReserve.get_courses()

    salas = []
    for sala in idsalas:
        salas.append(Classroom.objects.get(id=sala))

    context = {
        "reservas": reservas,
        "professores": professores,
        "cursos": courses,
        "salas": salas,
        "turmas": turmas,
        "periodos": periodos,
    }
    get_dash_context(context, "Períodos", "editar_periodo")
    return render(request, "periodo/dashboard.periodo.historico.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def list_periods(request):
    course = request.GET.get("course")
    period = request.GET.get("period")
    class_period = request.GET.get("class_period")

    base = PeriodReserve.objects.all()
    if course:
        base = base.filter(course=course)
    if period:
        base = base.filter(period=period)
    if class_period:
        base = base.filter(class_period=class_period)

    groups = (
        base.exclude(course__isnull=True)
        .values("course", "period", "class_period")
        .order_by()
        .annotate(
            period_total=Count("period"),
            course_total=Count("course"),
            class_period_total=Count("class_period"),
        )
    )

    period_groups = []
    courses = PeriodReserve.get_courses()
    for group in groups:
        periods = PeriodReserve.objects.filter(
            course=group["course"],
            period=group["period"],
            class_period=group["class_period"],
        )
        date_begin = (
            periods.values("date_begin")
            .annotate(Min("date_begin"))
            .order_by("date_begin")[0]["date_begin__min"]
        )

        for index, name in courses:
            if group["course"] == index:
                course_name = name

        period_groups.append(
            {
                "course": course_name,
                "period": group["period"],
                "class_period": group["class_period"],
                "date_begin": date_begin,
                "periods": periods,
            }
        )

    reservas = PeriodReserve.objects.all()
    turmas = (
        reservas.order_by("class_period")
        .values_list("class_period", flat=True)
        .distinct()
    )
    periodos = reservas.order_by("period").values_list("period", flat=True).distinct()
    courses = PeriodReserve.get_courses()

    context = {
        "period_groups": period_groups,
        "cursos": courses,
        "turmas": turmas,
        "periodos": periodos,
    }
    get_dash_context(context, "Períodos", "periodo_relatorio")
    return render(request, "periodo/dashboard.periodo.lista.html", context)


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=periodo_roles)
def update_period(request, pk):
    period = PeriodReserve.objects.get(id=pk)
    salas = Classroom.objects.all()
    cursos = PeriodReserve.get_courses()
    context = {"period": period, "salas": salas, "cursos": cursos}
    return render(request, "periodo/dashboard.periodo.editar.html", context)
