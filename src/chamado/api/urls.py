from django.urls import include, path
from rest_framework import routers

from chamado.api.viewsets import ChamadoAdminViewSet, ChamadoViewSet

router = routers.DefaultRouter()

router.register(r"chamados", ChamadoViewSet, basename="chamado")
router.register(r"admin/chamados", ChamadoAdminViewSet, basename="chamado_admin")

urlpatterns = [path("", include(router.urls))]
