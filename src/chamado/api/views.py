from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import StdResultsSetPagination
from chamado.api.permissions import GroupSuporte
from chamado.api.serializers import ChamadoCreateSerializer, ChamadoSerializer
from chamado.models import Chamado


class ChamadoViewSet(viewsets.ModelViewSet):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
    pagination_class = StdResultsSetPagination
    permission_classes = [
        IsAuthenticated,
        GroupSuporte,
    ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "status": ["exact", "in"],
    }
    ordering_fields = ["created"]

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[AllowAny],
        serializer_class=ChamadoCreateSerializer,
    )
    def open(self, request, pk=None):
        serializer_cls = self.get_serializer_class()
        serializer = serializer_cls(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
