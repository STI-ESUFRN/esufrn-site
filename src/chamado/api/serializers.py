from rest_framework import serializers

from chamado.models import Chamado, Sala


class ChamadoCreateSerializer(serializers.ModelSerializer):
    sala = serializers.PrimaryKeyRelatedField(
        queryset=Sala.objects.all(),
        required=False,
        allow_null=True,
    )
    sala_outros = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Chamado
        fields = [
            "equipment",
            "tombamento",
            "description",
            "requester",
            "sala",
            "sala_outros",
            "date",
            "responsible_technician",
            "obs",
            "status",
        ]

    def validate(self, attrs):
        # Usamos pop com default para garantir que capturamos o valor ou definimos um padrão
        sala = attrs.get("sala", None)
        sala_outros = (attrs.get("sala_outros") or "").strip()

        # Validação caso ambos estejam vazios
        if sala is None and not sala_outros:
            raise serializers.ValidationError({"sala": "Selecione uma sala ou informe em Outros."})

        # SE FOI ESCOLHIDA UMA SALA CADASTRADA
        if sala is not None:
            attrs["sala"] = sala          # Garante o objeto Sala no dicionário
            attrs["sala_outros"] = ""     # Limpa o texto de outros

        # SE FOI INFORMADO "OUTROS"
        else:
            attrs["sala"] = None          # Força a Foreign Key a ser Nula
            attrs["sala_outros"] = sala_outros # Define o texto digitado

        return attrs


class ChamadoSerializer(serializers.ModelSerializer):
    sala = serializers.SerializerMethodField()

    class Meta:
        model = Chamado
        fields = [
            "id",
            "equipment",
            "tombamento",
            "description",
            "requester",
            "sala",
            "sala_outros",
            "date",
            "responsible_technician",
            "solved_at",
            "obs",
            "status",
            "created",
            "modified",
            "is_removed",
        ]

    def get_sala(self, obj):
        return obj.get_room_display()
