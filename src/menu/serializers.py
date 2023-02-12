from rest_framework import serializers

from menu.models import Itens, SubItens


class SubitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubItens
        fields = [
            "id",
            "name",
            "link",
            "order",
            "decoration",
        ]


class ItemSerializer(serializers.ModelSerializer):
    subitems = SubitemSerializer(many=True)

    class Meta:
        model = Itens
        fields = [
            "id",
            "name",
            "action_type",
            "subitems",
            "footer",
            "link",
            "order",
            "decoration",
        ]
