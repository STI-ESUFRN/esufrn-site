from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from core.fields import MultiSelectField, PrimaryKeyRelatedFieldWithSerializer
from reserva.enums import Shift
from reserva.models import Classroom, Period, Reserve, ReserveDay


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
        if "classroom" in self.context["request"].data:
            classroom = Classroom.objects.get(
                id=self.context["request"].data["classroom"]
            )
            if classroom.justification_required and not cause:
                raise ValidationError(
                    "Este tipo de sala requer que o usuário informe uma justificativa"
                    " para seu uso."
                )
        return cause

    def validate_declare(self, declare):
        if "classroom" in self.context["request"].data:
            classroom = Classroom.objects.get(
                id=self.context["request"].data["classroom"]
            )
            if classroom.type == "lab" and not self.context["request"].data.get(
                "declare", False
            ):
                raise ValidationError(
                    "Este tipo de sala requer que o usuário declare que esteja presente"
                    " um docente no momento da aula."
                )
        return declare

    def validate_date(self, date):
        if "shift" in self.context["request"].data:
            if self.context["request"].data["shift"] == "M":
                time = "12:30"
            elif self.context["request"].data["shift"] == "T":
                time = "18:30"
            else:
                time = "22:15"

            relative_date = datetime.strptime(
                f"{self.context['request'].data['date']} {time}", "%Y-%m-%d %H:%M"
            )
            now = datetime.today()

            diff = (relative_date - now).days
            if diff < 0:
                raise ValidationError(
                    "Você não pode reservar uma sala para uma data passada."
                )

            if "classroom" in self.context["request"].data:
                classroom = Classroom.objects.get(
                    id=self.context["request"].data["classroom"]
                )
                if diff < classroom.days_required:
                    raise ValidationError(
                        "A reserva para esta sala requer antecedência de"
                        f" {classroom.days_required} "
                        f"dia{'s' if classroom.days_required > 1 else ''}."
                    )

        return date


class CreateReserveSerializer(ReserveSerializer):
    class Meta:
        model = Reserve
        fields = [
            "classroom",
            "date",
            "event",
            "shift",
            "cause",
            "equipment",
            "requester",
            "email",
            "phone",
            "declare",
        ]


class ReservePublicSerializer(ReserveSerializer):
    classroom = PrimaryKeyRelatedFieldWithSerializer(
        ClassroomSerializer, queryset=Classroom.objects.all()
    )
    shift_display = serializers.CharField(source="get_shift_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Reserve
        fields = [
            "id",
            "date",
            "classroom",
            "event",
            "status",
            "status_display",
            "shift",
            "shift_display",
        ]
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
        }


class PeriodSerializer(serializers.ModelSerializer):
    classroom = PrimaryKeyRelatedFieldWithSerializer(
        ClassroomSerializer, queryset=Classroom.objects.all()
    )
    shift = MultiSelectField(choices=Shift.choices)
    weekdays = MultiSelectField(choices=Period.Weekdays.choices)
    course_display = serializers.CharField(source="get_course_display", read_only=True)

    class Meta:
        model = Period
        fields = [
            "id",
            "classroom",
            "status",
            "date_begin",
            "date_end",
            "workload",
            "weekdays",
            "classname",
            "classcode",
            "course",
            "course_display",
            "period",
            "class_period",
            "shift",
            "requester",
            "email",
            "phone",
            "equipment",
            "obs",
        ]

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.Meta.model.objects.ensure_days(instance)
        return instance


class ReserveDaySerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReserveDay
        fields = [
            "id",
            "date",
            "shift",
            "classroom",
            "active",
            "status",
            "event",
        ]
