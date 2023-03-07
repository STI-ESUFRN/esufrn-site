from django.urls import include, path
from rest_framework_nested import routers

from reserva.api.views import (
    CalendarViewSet,
    PeriodViewset,
    ReserveDayViewSet,
    ReserveViewSet,
)

app_name = "reserves"


router = routers.SimpleRouter()
router.register("calendar", CalendarViewSet, basename="calendar")
router.register("periods", PeriodViewset, basename="periodos")
router.register("reserves", ReserveViewSet, basename="reservas")

period_router = routers.NestedSimpleRouter(router, "periods", lookup="period")
period_router.register("days", ReserveDayViewSet, basename="days")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(period_router.urls)),
]
