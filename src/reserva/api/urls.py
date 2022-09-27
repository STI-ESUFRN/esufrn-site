from django.urls import path

from reserva.api.views import (
    calendarioView,
    periodAdminView,
    periodDayAdminView,
    periodDaysAdminView,
    periodsAdminView,
    reservaAdminView,
    reservasAdminView,
    reservasView,
)

urlpatterns = [
    path("calendario", calendarioView.as_view()),  # (PÚBLICO) get
    path("admin/reservas", reservasAdminView.as_view()),  # get, post
    path("admin/reservas/<int:pk>", reservaAdminView.as_view()),  # get, put, delete
    path("reservas", reservasView.as_view()),  # get, (PÚBLICO) post
    path("admin/periodos", periodsAdminView.as_view()),  # get, post
    path(
        "admin/periodos/<int:period_pk>", periodAdminView.as_view()
    ),  # get, put, delete
    path("admin/periodos/<int:period_pk>/dias", periodDaysAdminView.as_view()),  # get
    path(
        "admin/periodos/<int:period_pk>/dias/<int:pk>", periodDayAdminView.as_view()
    ),  # get, put
]
