from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from api.pagination import StdResultsSetPagination
from chamado.models import Chamado

from .permissions import GroupSuporte
from .serializers import ChamadoAdminSerializer, ChamadoSerializer


class ChamadoViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChamadoSerializer


class ChamadoAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ChamadoAdminSerializer
    queryset = Chamado.objects.all()
    pagination_class = StdResultsSetPagination
    permission_classes = [
        IsAuthenticated,
        GroupSuporte,
    ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "status": ["exact"],
    }
    ordering_fields = ["date"]

    # def get_queryset(self):
    #     queryset = Chamado.objects.all()

    #     options = self.request.query_params.get("options")
    #     if options is not None:
    #         options_list = options.split(",")
    #         if "hist" in options_list:
    #             queryset = queryset.exclude(status__isnull=True)

    #     status = self.request.query_params.get("status")
    #     if status is not None:
    #         queryset = queryset.filter(
    #             status=True if status == "A" else False if status == "R" else None
    #         )

    #     return queryset
