from django.urls import include, path
from rest_framework.routers import DefaultRouter

from laboratorio.views import MaterialViewSet

app_name = "laboratorio"

router = DefaultRouter()

router.register("materiais", MaterialViewSet, basename="materials")


urlpatterns = [
    path("", include(router.urls)),
]
