from django.contrib.auth import views as auth_views
from django.urls import include, path

from dashboard.views import ResetPasswordView, home_view, login_view, logout_view

urlpatterns = [
    path("", home_view, name="dashboard_home"),
    path("reserva/", include("dashboard.reserva.urls")),
    path("chamado/", include("dashboard.chamado.urls")),
    path("periodo/", include("dashboard.periodo.urls")),
    path("laboratorio/", include("dashboard.laboratorio.urls")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
]
