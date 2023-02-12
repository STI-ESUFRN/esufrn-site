from django.urls import include, path
from rest_framework.routers import DefaultRouter

from laboratorio.views import CategoryViewSet, ConsumableViewSet, PermanentViewSet

app_name = "laboratory"

router = DefaultRouter()

router.register("consumables", ConsumableViewSet, basename="consumables")
router.register("permanents", PermanentViewSet, basename="permanents")
router.register("categories", CategoryViewSet, basename="categories")


urlpatterns = [
    path("", include(router.urls)),
]
