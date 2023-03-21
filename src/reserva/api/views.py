from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsSafeMethods, IsSuperAdmin
from reserva.api.filters import CalendarFilter
from reserva.api.permissions import IsFromCoordination, IsFromDirection, IsFromReserve
from reserva.enums import Status
from reserva.models import Classroom, Period, Reserve, ReserveDay
from reserva.serializers import (
    ClassroomSerializer,
    CreateReserveSerializer,
    PeriodSerializer,
    ReserveDaySerializer,
    ReserveSerializer,
)


class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = Reserve.available_objects.all()
    permission_classes = [
        IsAuthenticated,
        IsFromReserve | IsSuperAdmin,
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "classroom": ["exact"],
        "status": ["exact"],
    }
    search_fields = [
        "event",
        "requester",
        "cause",
        "equipment",
        "obs",
        "email_response",
    ]
    ordering_fields = ["created"]

    def get_serializer_class(self):
        if self.action == "cadastrar":
            return CreateReserveSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset

        classrooms = self.request.user.classrooms.all().values("classroom")
        return queryset.filter(classroom__in=classrooms)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def cadastrar(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset).filter(status=Status.WAITING)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def historico(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset).exclude(status=Status.WAITING)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PeriodViewset(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsFromCoordination | IsFromDirection | IsSuperAdmin,
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = {
        "classroom": ["exact"],
        "status": ["exact"],
        "date_begin": ["exact", "range"],
        "date_end": ["exact", "range"],
        "workload": ["exact"],
        "course": ["exact"],
        "shift": ["exact", "icontains"],
    }
    search_fields = [
        "weekdays",
        "classname",
        "classcode",
        "period",
        "class_period",
        "requester",
        "email",
        "phone",
        "equipment",
        "obs",
    ]


class ReserveDayViewSet(viewsets.ModelViewSet):
    queryset = ReserveDay.objects.all()
    serializer_class = ReserveDaySerializer
    pagination_class = None
    permission_classes = [
        (AllowAny & IsSafeMethods)
        | (IsAuthenticated & (IsFromCoordination | IsFromDirection | IsSuperAdmin)),
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "date": ["exact", "month", "year", "range"],
        "shift": ["exact"],
        "classroom": ["exact"],
    }

    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())
        return queryset.filter(period=self.kwargs["period_pk"])


class ClassroomViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_anonymous:
            return queryset.filter(public=True)

        return queryset


class CalendarViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReserveDaySerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filter_class = CalendarFilter

    def get_queryset(self):
        queryset = ReserveDay.objects.filter(
            Q(period__status=Status.APPROVED)
            | Q(reserve__status=Status.APPROVED)
            | Q(period__status=Status.WAITING)
            | Q(reserve__status=Status.WAITING),
            active=True,
        )
        return self.filter_queryset(queryset)
