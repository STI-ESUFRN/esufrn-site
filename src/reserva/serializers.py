from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from core.fields import PrimaryKeyRelatedFieldWithSerializer
from reserva.models import Classroom, PeriodReserve, PeriodReserveDay, Reserve


class ClassroomSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    floor_display = serializers.CharField(source="get_floor_display", read_only=True)

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "full_name",
            "acronym",
            "type",
            "type_display",
            "number",
            "days_required",
            "justification_required",
            "floor",
            "floor_display",
        ]


class ReserveSerializer(serializers.ModelSerializer):
    classroom = PrimaryKeyRelatedFieldWithSerializer(
        ClassroomSerializer, queryset=Classroom.objects.all()
    )
    shift_display = serializers.CharField(source="get_shift_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Reserve
        fields = [
            "id",
            "classroom",
            "date",
            "event",
            "shift",
            "shift_display",
            "cause",
            "equipment",
            "requester",
            "email",
            "phone",
            "status",
            "status_display",
            "obs",
            "email_response",
            "declare",
            "admin_created",
            "created",
            "modified",
            "is_removed",
        ]
        extra_kwargs = {
            "admin_created": {
                "read_only": True,
            },
        }

    def validate_cause(self, cause):
        classroom = Classroom.objects.get(id=self.context["request"].data["classroom"])
        if classroom.justification_required and not self.cause:
            raise ValidationError(
                "Este tipo de sala requer que o usuário informe uma justificativa"
                " para seu uso."
            )
        return cause

    def validate_declare(self, declare):
        classroom = Classroom.objects.get(id=self.context["request"].data["classroom"])
        if classroom.type == "lab" and not self.context["request"].data["declare"]:
            raise ValidationError(
                "Este tipo de sala requer que o usuário declare que esteja presente"
                " um docente no momento da aula."
            )
        return declare

    def validate_date(self, date):
        if self.context["request"].data["shift"] == "M":
            time = "12:30"
        elif self.context["request"].data["shift"] == "T":
            time = "18:30"
        else:
            time = "22:15"

        relative_date = datetime.strptime(
            "{} {}".format(self.context["request"].data["date"], time), "%Y-%m-%d %H:%M"
        )
        now = datetime.today()

        diff = (relative_date - now).days
        if diff < 0:
            raise ValidationError(
                "Você não pode reservar uma sala para uma data passada."
            )

        classroom = Classroom.objects.get(id=self.context["request"].data["classroom"])
        if diff < classroom.days_required:
            raise ValidationError(
                "A reserva para esta sala requer antecedência de {} dia{}.".format(
                    classroom.days_required,
                    "s" if classroom.days_required > 1 else "",
                )
            )

        return date

    def validate_status(self, status):
        if self.instance and self.instance.status == Reserve.Status.APPROVED:
            reserves = Reserve.objects.filter(
                date=self.instance.date,
                status=Reserve.Status.APPROVED,
                classroom=self.instance.classroom,
                shift=self.instance.shift,
            ).exclude(id=self.instance.id)
            periodreserves = PeriodReserveDay.objects.filter(
                date=self.instance.date,
                period__status=Reserve.Status.APPROVED,
                period__classroom=self.instance.classroom,
                shift=self.instance.shift,
            ).exclude(active=False)

            if reserves or periodreserves:
                raise ValidationError(
                    "Já existe uma reserva aprovada para o dia {} - {}{}".format(
                        self.instance.date.strftime("%d/%m/%Y"),
                        self.instance.get_shift_name(),
                        "."
                        if self.instance.admin_created
                        else (
                            ". Por favor, entre em contato com a secretaria a fim de"
                            " viabilizarmos outro dia para esta reserva."
                        ),
                    )
                )

        return status


class ReservePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = [
            "date",
            "classroom",
            "event",
            "status",
            "shift",
        ]
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
        }


class PeriodReserveDaySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.period.status

    shift_name = serializers.SerializerMethodField()

    def get_shift_name(self, obj):
        return obj.get_shift_name()

    event = serializers.SerializerMethodField()

    def get_event(self, obj):
        return str(obj.period)

    class Meta:
        model = PeriodReserveDay
        exclude = ()
        fields = "__all__"


class PeriodReserveDayPublicSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.period.status

    shift_name = serializers.SerializerMethodField()

    def get_shift_name(self, obj):
        return obj.get_shift_name()

    event = serializers.SerializerMethodField()

    def get_event(self, obj):
        return str(obj.period)

    class Meta:
        model = PeriodReserveDay
        fields = ["status", "event", "date", "shift", "shift_name"]


class PeriodReserveBasicSerializer(serializers.ModelSerializer):
    classroom = serializers.SerializerMethodField()

    def get_classroom(self, obj):
        classroom = Classroom.objects.get(id=obj.classroom.id)
        serializer = ClassroomSerializer(classroom, many=False)
        return serializer.data

    course_name = serializers.SerializerMethodField()

    def get_course_name(self, obj):
        return obj.get_course_name()

    class Meta:
        model = PeriodReserve
        exclude = ()
        fields = "__all__"
