from django.urls import include, path
from rest_framework.routers import DefaultRouter

from laboratorio.api.views import (
    CategoryViewSet,
    ConsumableViewSet,
    PermanentViewSet,
    WarehouseViewSet,
    CategoryViewSetTI,  # Importe as novas views _TI
    ConsumableViewSetTI,
    PermanentViewSetTI,
    WarehouseViewSetTI,
)

app_name = "laboratory"

router = DefaultRouter()

# URLs para as views originais
router.register("consumables", ConsumableViewSet, basename="consumables")
router.register("permanents", PermanentViewSet, basename="permanents")
router.register("categories", CategoryViewSet, basename="categories")
router.register("warehouses", WarehouseViewSet, basename="warehouses")

# URLs para as views duplicadas (TI)
router.register("ti/consumables", ConsumableViewSetTI, basename="ti_consumables")
router.register("ti/permanents", PermanentViewSetTI, basename="ti_permanents")
router.register("ti/categories", CategoryViewSetTI, basename="ti_categories")
router.register("ti/warehouses", WarehouseViewSetTI, basename="ti_warehouses")

urlpatterns = [
    path("laboratory/", include(router.urls)),
]