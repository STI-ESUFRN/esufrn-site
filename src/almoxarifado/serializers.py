from rest_framework import serializers

from almoxarifado.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "expiration",
            "type",
            "quantity",
            "received_date",
            "created",
            "modified",
            "is_removed",
        ]
