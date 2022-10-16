from rest_framework import serializers

from chamado.models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "title",
            "description",
            "requester",
            "course",
            "contact",
        ]


class ChamadoAdminSerializer(serializers.ModelSerializer):
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
        ]
