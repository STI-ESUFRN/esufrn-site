from django.contrib.auth import views as auth_views
from django.urls import path

from dashboard.views import (
    ResetPasswordView,
    chamadoHistorico,
    chamadoHome,
    chamadoInserir,
    dashboardHome,
    inventarioEmprestimo,
    inventarioHome,
    inventarioPatrimonio,
    loginView,
    logoutView,
    materialConsumivelHome,
    materialEditar,
    materialInserirMaterialConsumivel,
    materialInserirMaterialPermanente,
    materialPermanenteHome,
    materialRelacao,
    periodoEditar,
    periodoHistorico,
    periodoHome,
    periodoInserir,
    periodoLista,
    reservaHistorico,
    reservaHome,
    reservaInserir,
    reservaRelatorio,
)

urlpatterns = [
    path("", dashboardHome, name="dashboard_home"),
    path("reserva/", reservaHome),
    path("reserva/historico/", reservaHistorico),
    path("reserva/inserir/", reservaInserir),
    path("reserva/relatorio/", reservaRelatorio),
    path("periodo/", periodoHome),
    path("periodo/historico/", periodoHistorico, name="periodo_historico"),
    path("periodo/inserir/", periodoInserir, name="periodo_inserir"),
    path("periodo/lista/", periodoLista, name="periodo_lista"),
    path("periodo/editar/<int:pk>/", periodoEditar, name="periodo_editar"),
    path("chamado/", chamadoHome),
    path("chamado/historico/", chamadoHistorico),
    path("chamado/inserir/", chamadoInserir),
    path("inventario/", inventarioHome),
    path("inventario/emprestimo", inventarioEmprestimo, name="inventario_emprestimo"),
    path("inventario/patrimonio", inventarioPatrimonio, name="inventario_patrimonio"),
    # path("laboratorio/", materialHome, name="material_home"),
    path("laboratorio/consumivel/", materialConsumivelHome),
    path("laboratorio/permanente/", materialPermanenteHome),
    path("laboratorio/relacao/", materialRelacao),
    path("laboratorio/item/<int:pk>/", materialEditar, name="material_editar"),
    path(
        "laboratorio/consumivel/inserir/",
        materialInserirMaterialConsumivel,
        name="material_consumivel_inserir",
    ),
    path(
        "laboratorio/permanente/inserir/",
        materialInserirMaterialPermanente,
        name="material_permanente_inserir",
    ),
    path("login/", loginView, name="login"),
    path("logout/", logoutView, name="logout"),
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
    # path("perfil/", pagePerfil),
]
