from django.db.models.deletion import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laboratorio.models import Category, Consumable, Permanent
from laboratorio.permissions import GroupLaboratorio
from laboratorio.serializers import (
    CategorySerializer,
    ConsumableSerializer,
    PermanentSerializer,
)


class ConsumableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, GroupLaboratorio]
    queryset = Consumable.available_objects.all()
    serializer_class = ConsumableSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "description", "comments", "brand", "location"]

    @action(detail=False, methods=["get"])
    def dashboard(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        obj = self.get_object()
        obj.quantity = obj.quantity + int(request.data["quantity"])
        if obj.quantity < 0:
            return Response(
                {"quantity": ["A quantidade do material não pode ser negativa"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj.create_log(request)
        obj.save()

        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, GroupLaboratorio]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)

        except ProtectedError as e:
            return Response(
                {
                    "non_field_errors": [
                        "Não foi possível apagar esta instância pois existem materiais"
                        " categorizados como tal."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response


class PermanentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, GroupLaboratorio]
    queryset = Permanent.available_objects.all()
    serializer_class = PermanentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "category": ["exact"],
    }
    search_fields = ["name", "number", "description", "comments", "brand", "location"]
