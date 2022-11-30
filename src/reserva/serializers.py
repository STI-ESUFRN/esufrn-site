from rest_framework import serializers

from core.fields import PrimaryKeyRelatedFieldWithSerializer
from reserva.models import Classroom, PeriodReserve, PeriodReserveDay, Reserve


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "full_name",
            "acronym",
            "type",
            "number",
            "days_required",
            "justification_required",
            "floor",
        ]


class ReserveSerializer(serializers.ModelSerializer):
    classroom = PrimaryKeyRelatedFieldWithSerializer(
        ClassroomSerializer, queryset=Classroom.objects.all()
    )

    class Meta:
        model = Reserve
        fields = [
            "id",
            "classroom",
            "date",
            "event",
            "shift",
            "cause",
            "equipment",
            "requester",
            "email",
            "phone",
            "status",
            "obs",
            "email_response",
            "declare",
            "admin_created",
            "created",
            "modified",
            "is_removed",
        ]


class ReservePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ("date", "classroom", "event", "status", "shift")


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
