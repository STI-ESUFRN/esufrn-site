from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Min
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from principal.decorators import (allowed_users, authenticated_user,
                                  unauthenticated_user)
from principal.forms import siginForm
from principal.models import Mensagem
from reserva.models import (Classroom, PeriodReserve, PeriodReserveDay,
                            Reserve, UserClassroom)

from .utils import getDashContext

# Create your views here.


# REGISTRATION
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'dashboard/registration/password_reset.html'
    email_template_name = 'dashboard/registration/password_reset_email.html'
    subject_template_name = 'dashboard/registration/password_reset_subject.txt'

    success_url = reverse_lazy('password_reset_done')


# LOGIN E LOGOUT
@unauthenticated_user(redirect_to="/dashboard")
@never_cache
def loginView(request):
    form = siginForm()

    if request.method == 'GET':
        context = {
            'form': form,
        }

    elif request.method == 'POST':
        username = request.POST.get('field_user_name', '')
        password = request.POST.get('field_passwd', '')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next = request.GET.get('next')
            if next:
                return redirect(next)

            return redirect("dashboard_home")
        else:
            context = {
                'status': 'error',
                'message': 'Credenciais inválidas',
                'form': form
            }

    return render(request, 'dashboard.login.html', context)


@authenticated_user(redirect_to="/dashboard/login")
def logoutView(request):
    logout(request)

    return redirect("login")


# HOME
@login_required(login_url='/dashboard/login')
def dashboardHome(request):
    messages = Mensagem.objects.all()
    now = datetime.now()

    shift = None
    if ((now.hour == 18 and now.minute >= 45) or now.hour > 18) and ((now.hour == 22 and now.minute <= 15) or now.hour < 22):
        shift = "N"
    elif now.hour >= 13 and ((now.hour == 18 and now.minute <= 30) or now.hour < 18):
        shift = "T"
    elif now.hour >= 7 and ((now.hour == 12 and now.minute <= 30) or now.hour < 12):
        shift = "M"

    events = []
    classes = []
    if shift:
        events = Reserve.objects.filter(
            date=now.date(), shift=shift, status="A")
        classes = PeriodReserveDay.objects.filter(
            date=now.date(), shift=shift, period__status="A", active=True)

    context = {
        "messages": messages[0: 3],
        "events": events,
        "classes": classes,

    }
    getDashContext(context, "Home")
    return render(request, "dashboard.home.html", context)


# CHAMADOS
chamados_roles = ['suporte']


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=chamados_roles)
def chamadoHome(request):
    context = {}
    getDashContext(context, "Chamados", "dashboard")
    return render(request, "dashboard.chamado.dashboard.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=chamados_roles)
def chamadoHistorico(request):
    context = {}
    getDashContext(context, "Chamados", "historico")
    return render(request, "dashboard.chamado.historico.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=chamados_roles)
def chamadoInserir(request):
    context = {}
    getDashContext(context, "Chamados", "chamado")
    return render(request, "dashboard.chamado.inserir.html", context)


# INVENTÁRIO
inventario_roles = ['suporte']


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=inventario_roles)
def inventarioHome(request):
    return redirect("inventario_emprestimo")


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=inventario_roles)
def inventarioEmprestimo(request):
    context = {}
    getDashContext(context, "Inventário", "inventario_emprestimo")
    return render(request, "dashboard.inventario.emprestimo.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=inventario_roles)
def inventarioPatrimonio(request):
    context = {}
    getDashContext(context, "Inventário", "inventario_patrimonio")
    return render(request, "dashboard.inventario.patrimonio.html", context)


# RESERVAS
reserva_roles = ['reserva', 'suporte']


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=reserva_roles)
def reservaHome(request):
    context = {}
    getDashContext(context, "Reservas", "reserva_dashboard")
    return render(request, "dashboard.reserva.dashboard.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=reserva_roles)
def reservaHistorico(request):
    context = {}
    getDashContext(context, "Reservas", "reserva_historico")
    return render(request, "dashboard.reserva.historico.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=reserva_roles)
def reservaInserir(request):
    user_classroomns = UserClassroom.objects.filter(
        user=request.user).values_list("classroom", flat=True)
    salas = Classroom.objects.filter(id__in=user_classroomns)
    context = {
        "salas": salas
    }
    getDashContext(context, "Reservas", "inserir_reserva")
    return render(request, "dashboard.reserva.inserir.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=reserva_roles)
def reservaRelatorio(request):
    salas = Classroom.objects.all()
    classroom_id = request.GET.get("classroom")
    sala = None
    if classroom_id is not None:
        sala = Classroom.objects.get(id=classroom_id)

    context = {
        "salas": salas,
        "sala": sala,
    }
    getDashContext(context, "Reservas", "relatorio")
    return render(request, "dashboard.reserva.relatorio.html", context)


# PERÍODOS
periodo_roles = ['reserva', 'suporte', 'coordenacao']


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=periodo_roles)
def periodoHome(request):
    return redirect("periodo_historico")


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=periodo_roles)
def periodoInserir(request):
    salas = Classroom.objects.all()
    cursos = PeriodReserve.get_courses()
    context = {
        "salas": salas,
        "cursos": cursos
    }
    getDashContext(context, "Períodos", "inserir_periodo")
    return render(request, "dashboard.periodo.inserir.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=periodo_roles)
def periodoHistorico(request):
    reservas = PeriodReserve.objects.all()

    professores = reservas.order_by(
        'requester').values_list('requester', flat=True).distinct()
    idsalas = reservas.order_by(
        'classroom').values_list('classroom', flat=True).distinct()
    turmas = reservas.order_by(
        'class_period').values_list('class_period', flat=True).distinct()
    periodos = reservas.order_by(
        'period').values_list('period', flat=True).distinct()

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
    getDashContext(context, "Períodos", "editar_periodo")
    return render(request, "dashboard.periodo.historico.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=periodo_roles)
def periodoLista(request):
    course = request.GET.get('course')
    period = request.GET.get('period')
    class_period = request.GET.get('class_period')

    base = PeriodReserve.objects.all()
    if course:
        base = base.filter(course=course)
    if period:
        base = base.filter(period=period)
    if class_period:
        base = base.filter(class_period=class_period)

    groups = (
        base.exclude(course__isnull=True)
        .values('course', 'period', 'class_period').order_by()
        .annotate(
            period_total=Count('period'),
            course_total=Count('course'),
            class_period_total=Count('class_period')
        )
    )

    period_groups = []
    courses = PeriodReserve.get_courses()
    for group in groups:
        periods = PeriodReserve.objects.filter(
            course=group['course'], period=group['period'], class_period=group['class_period'])
        date_begin = periods.values('date_begin').annotate(
            Min('date_begin')).order_by('date_begin')[0]['date_begin__min']

        for index, name in courses:
            if group['course'] == index:
                course_name = name

        period_groups.append({
            "course": course_name,
            "period": group['period'],
            "class_period": group['class_period'],
            "date_begin": date_begin,
            "periods": periods
        })

    reservas = PeriodReserve.objects.all()
    turmas = reservas.order_by(
        'class_period').values_list('class_period', flat=True).distinct()
    periodos = reservas.order_by(
        'period').values_list('period', flat=True).distinct()
    courses = PeriodReserve.get_courses()

    context = {
        "period_groups": period_groups,
        "cursos": courses,
        "turmas": turmas,
        "periodos": periodos,
    }
    getDashContext(context, "Períodos", "periodo_relatorio")
    return render(request, "dashboard.periodo.lista.html", context)


@login_required(login_url='/dashboard/login')
@allowed_users(allowed_roles=periodo_roles)
def periodoEditar(request, pk):
    period = PeriodReserve.objects.get(id=pk)
    salas = Classroom.objects.all()
    cursos = PeriodReserve.get_courses()
    context = {
        "period": period,
        "salas": salas,
        "cursos": cursos
    }
    return render(request, "dashboard.periodo.editar.html", context)
