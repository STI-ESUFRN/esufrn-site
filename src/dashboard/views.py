from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

from dashboard.forms import SiginForm
from dashboard.helpers import get_dash_context
from principal.decorators import authenticated_user, unauthenticated_user
from principal.models import Message
from reserva.models import Reserve, ReserveDay


# REGISTRATION
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "dashboard/registration/password_reset.html"
    email_template_name = "dashboard/registration/password_reset_email.html"
    subject_template_name = "dashboard/registration/password_reset_subject.txt"

    success_url = reverse_lazy("password_reset_done")


# LOGIN E LOGOUT
@unauthenticated_user(redirect_to="/dashboard")
@never_cache
def login_view(request):
    form = SiginForm()

    if request.method == "GET":
        context = {
            "form": form,
        }

    elif request.method == "POST":
        username = request.POST.get("field_user_name", "")
        password = request.POST.get("field_passwd", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("dashboard_home")
        else:
            context = {
                "status": "error",
                "message": "Credenciais inválidas",
                "form": form,
            }

    return render(request, "dashboard.login.html", context)


@authenticated_user(redirect_to="/dashboard/login")
def logout_view(request):
    logout(request)

    return redirect("login")


# HOME
@login_required(login_url="/dashboard/login")
def home_view(request):
    messages = Message.objects.all()
    now = datetime.now()

    shift = None
    if ((now.hour == 18 and now.minute >= 45) or now.hour > 18) and (
        (now.hour == 22 and now.minute <= 15) or now.hour < 22
    ):
        shift = "N"
    elif now.hour >= 13 and ((now.hour == 18 and now.minute <= 30) or now.hour < 18):
        shift = "T"
    elif now.hour >= 7 and ((now.hour == 12 and now.minute <= 30) or now.hour < 12):
        shift = "M"

    events = []
    classes = []
    if shift:
        events = Reserve.objects.filter(date=now.date(), shift=shift, status="A")
        classes = ReserveDay.objects.filter(
            date=now.date(), shift=shift, period__status="A", active=True
        )

    context = {
        "messages": messages[0:3],
        "events": events,
        "classes": classes,
    }
    get_dash_context(context, "Home")
    return render(request, "dashboard.home.html", context)
