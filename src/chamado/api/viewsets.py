from chamado.models import Chamado
from rest_framework import mixins, viewsets

from api.pagination import StdResultsSetPagination

from .permissions import GroupSuporte
from .serializers import ChamadoAdminSerializador, ChamadoSerializador


class ChamadoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ChamadoSerializador


class ChamadoAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [GroupSuporte, ]

    def get_queryset(self):
        queryset = Chamado.objects.all()

        options = self.request.query_params.get('options')
        if options is not None:
            options_list = options.split(',')
            if "hist" in options_list:
                queryset = queryset.exclude(status__isnull=True)

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(
                status=True if status == 'A' else False if status == 'R' else None)

        order = self.request.query_params.get("order")
        if order is not None:
            queryset = queryset.order_by(
                'date' if order == 'dec' else '-date')

        return queryset

    serializer_class = ChamadoAdminSerializador
    pagination_class = StdResultsSetPagination
