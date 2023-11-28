from rest_framework import serializers

from chamado.models import Chamado


class ChamadoCreateSerializer(serializers.ModelSerializer):
    shift = serializers.CharField(required=True, allow_null=False)
    concorda = serializers.CharField(required=True, allow_null=False)
    # presenca = serializers.BooleanField(required=True, allow_null=False)

    class Meta:
        model = Chamado
        fields = [
            "title",
            "description",
            "requester",
            "course",
            "contact",
            "date",
            "shift",
            "concorda",
        ]


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "id",
            "title",
            "description",
            "requester",
            "course",
            "contact",
            "solved_at",
            "obs",
            "status",
            "created",
            "modified",
            "is_removed",
            "date",
            "shift",
            "concorda",
        ]
