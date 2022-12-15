from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from api.pagination import StdResultsSetPagination
from chamado.api.permissions import GroupSuporte
from chamado.api.serializers import ChamadoAdminSerializer, ChamadoSerializer
from chamado.models import Chamado


class ChamadoViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ChamadoSerializer


from rest_framework.permissions import AllowAny


class ChamadoAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ChamadoAdminSerializer
    queryset = Chamado.objects.all()
    pagination_class = StdResultsSetPagination
    permission_classes = [
        IsAuthenticated & GroupSuporte,
        # AllowAny
    ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "status": ["exact"],
    }
    ordering_fields = ["created"]

    def get_queryset(self):
        queryset = super().get_queryset()

        options = self.request.query_params.get("options")
        if options is not None:
            options_list = options.split(",")
            if "hist" in options_list:
                queryset = queryset.exclude(status=Chamado.Status.PENDING)

        return queryset
