from django.urls import include, path
from rest_framework.routers import DefaultRouter

from laboratorio.api.views import (
    CategoryViewSet,
    ConsumableViewSet,
    PermanentViewSet,
    WarehouseViewSet,
)

app_name = "laboratory"

router = DefaultRouter()

router.register("consumables", ConsumableViewSet, basename="consumables")
router.register("permanents", PermanentViewSet, basename="permanents")
router.register("categories", CategoryViewSet, basename="categories")
router.register("warehouses", WarehouseViewSet, basename="warehouses")


urlpatterns = [
    path("laboratory/", include(router.urls)),
]
