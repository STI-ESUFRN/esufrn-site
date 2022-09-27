from django.urls import path

from inventario.api.views import (
    emprestimoPatrimoniosView,
    emprestimosView,
    emprestimoView,
    maquinasView,
    patrimoniosView,
)

urlpatterns = [
    path("admin/patrimonios", patrimoniosView.as_view()),
    path("admin/emprestimos", emprestimosView.as_view()),
    path("admin/emprestimos/<int:pk>", emprestimoView.as_view()),
    path("admin/emprestimos/<int:pk>/patrimonios", emprestimoPatrimoniosView.as_view()),
    path("admin/maquinas", maquinasView.as_view()),
    path("admin/maquinas/<int:pk>", patrimoniosView.as_view()),
]
