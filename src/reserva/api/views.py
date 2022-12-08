import math
from datetime import datetime
from functools import reduce

from django.db.models import Q
from django.forms import ValidationError
from django.http import Http404, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from principal.decorators import allowed_users
from principal.helpers import haveMore, paginate
from reserva.models import (
    Classroom,
    PeriodReserve,
    PeriodReserveDay,
    Reserve,
    UserClassroom,
)
from reserva.serializers import (
    PeriodReserveBasicSerializer,
    PeriodReserveDayPublicSerializer,
    PeriodReserveDaySerializer,
    ReservePublicSerializer,
    ReserveSerializer,
)


class IsFromReserve(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="reserva").exists()


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class ReservaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReserveSerializer
    queryset = Reserve.available_objects.all()
    permission_classes = [
        IsAuthenticated,
        IsFromReserve | IsSuperAdmin,
    ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "classroom__id": ["exact"],
        "status": ["exact"],
        "created": ["exact", "lte", "gte"],
    }
    ordering_fields = ["created"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()

        classrooms = self.request.user.classrooms.all().values("classroom")
        return super().get_queryset().filter(classroom__in=classrooms)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def cadastrar(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def historico(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset()).filter(
            status__in=[Reserve.Status.REJECTED, Reserve.Status.APPROVED]
        )
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard(self, request, pk=None):
        queryset = self.get_queryset().filter(status=Reserve.Status.WAITING)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


reserve_decorators = [
    allowed_users(allowed_roles=["reserva"]),
]
period_decorators = [
    allowed_users(allowed_roles=["reserva", "coordenacao"]),
]


class calendarioView(View):
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        year = request.GET.get("year", str(now.date().year))
        month = request.GET.get("month", str(now.date().month))

        reserves = Reserve.objects.filter(date__year=year, date__month=month)
        periodreserves = PeriodReserveDay.objects.filter(
            date__year=year, date__month=month
        ).exclude(active=False)

        if request.GET.get("classroom"):
            reserves = reserves.filter(classroom=request.GET.get("classroom"))
            periodreserves = periodreserves.filter(
                period__classroom=request.GET.get("classroom")
            )

        if request.GET.get("status"):
            reserves = reserves.filter(status=request.GET.get("status"))
            periodreserves = periodreserves.filter(
                period__status=request.GET.get("status")
            )

        if request.GET.get("shift"):
            reserves = reserves.filter(shift=request.GET.get("shift"))
            periodreserves = periodreserves.filter(shift=request.GET.get("shift"))

        else:
            reserves = reserves.exclude(status="R")
            periodreserves = periodreserves.exclude(period__status="R")

        try:
            data_reserves = []
            if reserves:
                serializador = ReservePublicSerializer(reserves, many=True)
                data_reserves += serializador.data

            if periodreserves:
                serializador = PeriodReserveDayPublicSerializer(
                    periodreserves, many=True
                )
                data_reserves += serializador.data

            return JsonResponse(data_reserves, safe=False)

        except Exception as e:
            return JsonResponse({"message": f"{str(e)}", "status": "error"}, safe=False)


# RESERVAS


@method_decorator(reserve_decorators, name="dispatch")
class reservasAdminView(View):
    def get(self, request, *args, **kwargs):
        orde = request.GET.get("orde", "dec")
        page = int(request.GET.get("page", "1"))

        mergeResult = []
        mergeJson = {"page": page, "total_page": 0, "have_more": False}

        npp = 8

        user = request.user
        if user.is_superuser:
            classrooms = Classroom.objects.all()
        else:
            classrooms = request.user.classrooms.all()

        reserves = (
            Reserve.objects.filter(classroom__in=classrooms)
            .exclude(status="E")
            .order_by("created" if orde == "dec" else "-created")
        )

        if request.GET.get("status"):
            reserves = reserves.filter(status=request.GET.get("status"))

        serializador = ReserveSerializer(paginate(reserves, page, npp), many=True)
        mergeResult += serializador.data

        mergeJson["have_more"] = haveMore(reserves.count(), npp, page)

        paginatedResults = [mergeResult] + [mergeJson]
        return JsonResponse(paginatedResults, safe=False)

    def post(self, request, *args, **kwargs):
        instClass = Classroom.objects.get(id=request.POST["classroom"])

        # date = datetime.strptime(request.POST["date"], "%d-%m-%Y").date()
        dates = request.POST.get("date").split(",")
        declare = True if request.POST.get("confirm") == "on" else False

        status = "A" if request.POST.get("status") == "on" else "E"

        reserves = []
        try:
            for date in dates:
                reserve = Reserve.objects.create(
                    classroom=instClass,
                    date=datetime.strptime(date, "%d-%m-%Y").date(),
                    event=request.POST["event"],
                    shift=request.POST["shift"],
                    equipment=request.POST["equipment"],
                    requester=request.POST["requester"],
                    email=request.POST["email"],
                    phone=request.POST["phone"],
                    status=status,
                    declare=declare,
                    obs=request.POST["obs"],
                    admin_created=True,
                )
                reserves.append(reserve)
            return JsonResponse(
                {
                    "message": "Solicitação cadastrada com sucesso!",
                    "status": "success",
                },
                safe=False,
            )

        except Exception as e:
            for reserve in reserves:
                reserve.delete()

            try:
                return JsonResponse(
                    {"message": "{}".format(next(iter(e))), "status": "error"},
                    safe=False,
                    status=200,
                )
            except:
                return JsonResponse(
                    {"message": "{}".format(e), "status": "error"},
                    safe=False,
                    status=200,
                )


class reservasView(View):
    @method_decorator(reserve_decorators)
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            classrooms = Classroom.objects.all()
        else:
            classrooms = UserClassroom.objects.filter(user=request.user).values_list(
                "classroom", flat=True
            )

        reserves = Reserve.objects.filter(classroom__in=classrooms, status="E")

        serializador = ReserveSerializer(reserves, many=True)
        return JsonResponse(serializador.data, safe=False)

    def post(self, request, *args, **kwargs):
        classroom = Classroom.objects.get(id=request.POST["classroom"])

        date = datetime.strptime(request.POST["date"], "%d-%m-%Y").date()

        try:
            Reserve.objects.create(
                classroom=classroom,
                date=date,
                event=request.POST["event"],
                shift=request.POST["shift"],
                equipment=request.POST["equipment"],
                requester=request.POST["requester"],
                email=request.POST["email"],
                phone=request.POST["phone"],
                cause=request.POST.get("cause"),
                declare=request.POST.get("confirm") == "on",
            )

            return JsonResponse(
                {
                    "message": (
                        "Solicitação realizada com sucesso! Espere a confirmação da"
                        " reserva por email."
                    ),
                    "status": "success",
                },
                safe=False,
            )

        except Exception as e:
            try:
                return JsonResponse(
                    {"message": "{}".format(next(iter(e))), "status": "error"},
                    safe=False,
                    status=200,
                )
            except:
                return JsonResponse(
                    {"message": "{}".format(e), "status": "error"},
                    safe=False,
                    status=200,
                )


# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(reserve_decorators, name="dispatch")
class reservaAdminView(View):
    def get(self, request, *args, **kwargs):
        try:
            result = Reserve.objects.get(id=kwargs["pk"])

            serializador = ReserveSerializer(result, many=False)
            return JsonResponse(serializador.data, safe=False)
        except Reserve.DoesNotExist:
            raise Http404()

    def put(self, request, *args, **kwargs):
        PUT = QueryDict(request.body)

        try:
            reserve = Reserve.objects.get(id=kwargs["pk"])

            status = PUT.get("status")
            msg = PUT.get("msg")
            if status is not None and status != reserve.status:
                reserve.update(status=status, email_response=msg)
                reserve.notify()

            obs = PUT.get("obs")
            if obs is not None:
                reserve.update(obs=obs)

            return JsonResponse(
                {"message": "Arquivo atualizado com sucesso!", "status": "success"},
                safe=False,
            )

        except Exception as e:
            try:
                return JsonResponse(
                    {"message": "{}".format(next(iter(e))), "status": "error"},
                    safe=False,
                )
            except:
                return JsonResponse(
                    {"message": "{}".format(e), "status": "error"}, safe=False
                )

    def delete(self, request, *args, **kwargs):
        try:
            Reserve.objects.get(id=self.kwargs["pk"]).delete()
            return JsonResponse(
                {"message": "Arquivo excluído com sucesso", "status": "success"}
            )

        except Exception as e:
            return JsonResponse({"message": e, "status": "error"})


# PERÍODOS
@method_decorator(period_decorators, name="dispatch")
class periodsAdminView(View):
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", "1"))

        npp = 8
        paginatorJSON = {"current": page, "total": 0, "npp": npp}

        try:
            result = PeriodReserve.objects.all()

            if request.GET.get("search"):
                words = request.GET.get("search").split()
                result = result.filter(
                    reduce(
                        lambda x, y: x & y,
                        [
                            (
                                Q(course__icontains=word)
                                | Q(classname__icontains=word)
                                | Q(requester__icontains=word)
                                | Q(phone__icontains=word)
                                | Q(email__icontains=word)
                            )
                            for word in words
                        ],
                    )
                )

            if request.GET.get("course"):
                result = result.filter(course=request.GET.get("course"))

            if request.GET.get("period"):
                result = result.filter(period=request.GET.get("period"))

            if request.GET.get("class_period"):
                result = result.filter(class_period=request.GET.get("class_period"))

            if request.GET.get("requester"):
                result = result.filter(
                    requester__icontains=request.GET.get("requester")
                )

            if request.GET.get("classroom"):
                result = result.filter(classroom=request.GET.get("classroom"))

            if request.GET.get("shift"):
                result = result.filter(shift__contains=request.GET.get("shift"))

            if request.GET.get("status"):
                result = result.filter(status=request.GET.get("status"))

            serializador = PeriodReserveBasicSerializer(
                paginate(result, page, npp), many=True
            )

            paginatorJSON["total"] = int(math.ceil(result.count() / npp))

            return JsonResponse(
                {"data": serializador.data, "paginator": paginatorJSON}, safe=False
            )

        except Exception as e:
            return JsonResponse(
                {"message": str(e), "status": "error"}, safe=False, status=200
            )

    def post(self, request, *args, **kwargs):
        classroom = Classroom.objects.get(id=request.POST["classroom"])
        date_begin = datetime.strptime(request.POST["date_begin"], "%d-%m-%Y")
        date_end = datetime.strptime(request.POST["date_end"], "%d-%m-%Y")
        weekdays = str(request.POST["week"]).split(",")
        shift = str(request.POST["shift"]).split(",")
        status = "A" if request.POST.get("status", None) == "on" else "E"
        workload = request.POST.get("workload")

        try:
            PeriodReserve.objects.create(
                classroom=classroom,
                status=status,
                date_begin=date_begin,
                date_end=date_end,
                workload=workload if workload else None,
                weekdays=weekdays,
                classname=request.POST["classname"],
                classcode=request.POST["classcode"],
                course=request.POST["course"],
                period=request.POST["period"],
                class_period=request.POST["class_period"],
                shift=shift,
                requester=request.POST["requester"],
                email=request.POST["email"],
                phone=request.POST["phone"],
                equipment=request.POST.get("equipment", None),
                obs=request.POST.get("obs", None),
            )

            return JsonResponse(
                {
                    "message": "Período cadastrado com sucesso!",
                    "status": "success",
                },
                safe=False,
            )

        except Exception as e:
            try:
                return JsonResponse(
                    {"message": "{}".format(next(iter(e))), "status": "error"},
                    safe=False,
                    status=200,
                )
            except:
                return JsonResponse(
                    {"message": "{}".format(e), "status": "error"},
                    safe=False,
                    status=200,
                )


@method_decorator(period_decorators, name="dispatch")
class periodAdminView(View):
    def get(self, request, *args, **kwargs):
        try:
            result = PeriodReserve.objects.get(id=kwargs["period_pk"])
            if result:
                serializador = PeriodReserveBasicSerializer(result, many=False)
                return JsonResponse(serializador.data, safe=False)

        except PeriodReserve.DoesNotExist:
            return JsonResponse(
                {"message": "Arquivo não esiste", "status": "error"},
                safe=False,
                status=200,
            )

    def put(self, request, *args, **kwargs):
        PUT = QueryDict(request.body)
        try:
            reserve = PeriodReserve.objects.get(id=self.kwargs["period_pk"])

            dic = PUT.dict()
            update_days = False

            if dic.get("date_begin"):
                dic["date_begin"] = datetime.strptime(
                    dic.get("date_begin"), "%d-%m-%Y"
                ).date()
                if dic["date_begin"] != reserve.date_begin:
                    update_days = True
            if dic.get("date_end"):
                dic["date_end"] = datetime.strptime(
                    dic.get("date_end"), "%d-%m-%Y"
                ).date()
                if dic["date_end"] != reserve.date_end:
                    update_days = True
            if dic.get("shift"):
                dic["shift"] = str(dic.get("shift")).split(",")
                if dic["shift"] != reserve.shift:
                    update_days = True

            if dic.get("week"):
                week = str(dic.get("week")).split(",")
                weekdays = []
                for i in week:
                    weekdays.append(i)
                list = []
                for i in reserve.weekdays:
                    list.append(i)

                dic["weekdays"] = weekdays
                if dic["weekdays"] != reserve.weekdays:
                    update_days = True

            if dic.get("classroom"):
                dic["classroom"] = Classroom.objects.get(id=int(dic.get("classroom")))
                if dic["classroom"] != reserve.classroom:
                    reserve.classroom = dic["classroom"]
                    update_days = True
                del dic["classroom"]

            if dic.get("workload") is not None and not dic["workload"]:
                del dic["workload"]

            reserve.update(**dic)

            if update_days:
                reserve.create_days()

            reserve.save()

            return JsonResponse(
                {"status": "success", "message": "Arquivo modificado com sucesso."}
            )

        except ValidationError as e:
            return JsonResponse(
                {"status": "error", "message": "{}".format(next(iter(e)))}
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": "{}".format(e)})

    def delete(self, request, *args, **kwargs):
        try:
            PeriodReserve.objects.get(id=self.kwargs["period_pk"]).delete()
            return JsonResponse(
                {"message": "Arquivo excluído com sucesso", "status": "success"}
            )

        except Exception as e:
            return JsonResponse({"message": e, "status": "error"})


@method_decorator(period_decorators, name="dispatch")
class periodDaysAdminView(View):
    def get(self, request, *args, **kwargs):
        days = PeriodReserveDay.objects.filter(period=kwargs["period_pk"]).order_by(
            "id"
        )
        serializador = PeriodReserveDaySerializer(days, many=True)

        return JsonResponse(serializador.data, safe=False)


@method_decorator(period_decorators, name="dispatch")
class periodDayAdminView(View):
    def get(self, request, *args, **kwargs):
        try:
            reserve = PeriodReserveDay.objects.get(
                period__id=kwargs["period_pk"], id=kwargs["pk"]
            )
            serializador = PeriodReserveDaySerializer(reserve, many=False)

            return JsonResponse(serializador.data, safe=False)

        except PeriodReserveDay.DoesNotExist:
            return JsonResponse(
                {"message": "Não existe", "status": "error"}, safe=False
            )

    def put(self, request, *args, **kwargs):
        PUT = QueryDict(request.body)
        try:
            reserve = PeriodReserveDay.objects.get(id=kwargs["pk"])

            status = PUT.get("status")
            if status is not None:
                reserve.update(active=True if status == "true" else False)

            return JsonResponse(
                {"status": "success", "message": "Arquivo modificado com sucesso."}
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "{}".format(next(iter(e)))}
            )
