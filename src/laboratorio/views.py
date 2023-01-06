from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laboratorio.models import Material
from laboratorio.permissions import GroupLaboratorio
from laboratorio.serializers import MaterialSerializer


class MaterialViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, GroupLaboratorio]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "type": ["exact"],
    }
    search_fields = ["name", "number", "description", "brand", "location"]

    @action(detail=False, methods=["get"])
    def dashboard(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
