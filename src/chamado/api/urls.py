from django.urls import include, path
from rest_framework import routers

from chamado.api.views import ChamadoViewSet

router = routers.DefaultRouter()

router.register("tickets", ChamadoViewSet, basename="chamado")

urlpatterns = [
    path("", include(router.urls)),
]
