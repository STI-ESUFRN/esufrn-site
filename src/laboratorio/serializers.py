from rest_framework import serializers
from rest_framework.serializers import ValidationError

from assets.models import ESImage
from assets.serializers import ESImageSerializer
from core.fields import PrimaryKeyRelatedFieldWithSerializer
from laboratorio.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    qr = PrimaryKeyRelatedFieldWithSerializer(
        ESImageSerializer, queryset=ESImage.objects.all(), required=False
    )

    class Meta:
        model = Material
        fields = [
            "id",
            "alert_below",
            "brand",
            "description",
            "expiration",
            "location",
            "name",
            "number",
            "qr",
            "quantity",
            "received_at",
            "reference",
            "type",
            "created",
            "modified",
        ]

    def validate_number(self, number):
        if (
            self.context["request"].data["type"] == Material.Types.PERMANENT
            and not number
        ):
            raise ValidationError(
                "Este tipo de material requer que seja especificado um número de"
                " tombamento",
                "permanent_non_specified_number",
            )

        return number

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.generate_qr(self.context["request"])

        return instance

    def update(self, instance, validated_data):
        instance.create_log(self.context["request"])

        return super().update(instance, validated_data)
