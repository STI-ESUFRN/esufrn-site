from django.urls import include, path
from rest_framework.routers import DefaultRouter

from almoxarifado.views import MaterialViewSet

app_name = "almoxarifado"

router = DefaultRouter()

router.register("materiais", MaterialViewSet, basename="materials")


urlpatterns = [
    path("", include(router.urls)),
]
