from django.urls import include, path
from rest_framework.routers import DefaultRouter

from almoxarifado.views import MaterialViewSet

router = DefaultRouter()

router.register("", MaterialViewSet, basename="materials")

urlpatterns = [
    path("", include(router.urls)),
]
