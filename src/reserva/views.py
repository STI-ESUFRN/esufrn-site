from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from principal.permissions import IsUserFromReserve, IsUserFromSupport
from reserva.models import Classroom, Reserve, UserClassroom
from reserva.serializers import ReserveSerializer


def homeReserva(request):
    salas = Classroom.objects.all()
    context = {
        "salas": salas,
        "crumbs": [{"name": "Informática"}, {"name": "Reserva de Salas"}],
    }

    return render(request, "informatica.reserva.inserir.html", context)


class ReserveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReserveSerializer
    permission_classes = [IsAuthenticated, IsUserFromSupport | IsUserFromReserve]
    queryset = Reserve.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            classrooms = Classroom.objects.all()
        else:
            classrooms = UserClassroom.objects.filter(user=user).values_list(
                "classroom", flat=True
            )

        return super().get_queryset().filter(classroom__in=classrooms, status="E")
