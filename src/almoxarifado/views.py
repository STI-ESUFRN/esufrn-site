from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from almoxarifado.models import Material
from almoxarifado.permissions import GroupAlmoxarifado
from almoxarifado.serializers import MaterialSerializer


class MaterialViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, GroupAlmoxarifado]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
