from rest_framework import serializers

from reserva.models import Classroom, PeriodReserve, PeriodReserveDay, Reserve


class ClassroomSerializer(serializers.ModelSerializer):
    classroom_name = serializers.SerializerMethodField()

    def get_classroom_name(self, obj):
        return obj.get_classroom_name()

    floor_name = serializers.SerializerMethodField()

    def get_floor_name(self, obj):
        return obj.get_floor_name()

    type_name = serializers.SerializerMethodField()

    def get_type_name(self, obj):
        return obj.get_type_name()

    class Meta:
        model = Classroom
        exclude = ()
        fields = "__all__"


class ReserveSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=False)

    shift_name = serializers.SerializerMethodField()

    def get_shift_name(self, obj):
        return obj.get_shift_name()

    status_name = serializers.SerializerMethodField()

    def get_status_name(self, obj):
        return obj.get_status_name()

    class Meta:
        model = Reserve
        exclude = ()
        fields = "__all__"


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
