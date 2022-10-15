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
        exclude = ["solved_at"]
