from rest_framework import serializers
from rest_framework.serializers import ValidationError

from assets.models import ESImage
from assets.serializers import ESImageSerializer
from core.fields import PrimaryKeyRelatedFieldWithSerializer
from core.serializers import UserSerializer
from laboratorio.models import Category, Consumable, History, Material, Permanent


class MaterialSerializer(serializers.ModelSerializer):
    qr_code = PrimaryKeyRelatedFieldWithSerializer(
        ESImageSerializer, queryset=ESImage.objects.all(), required=False
    )

    class Meta:
        model = Material
        fields = [
            "id",
            "name",
            "description",
            "brand",
            "received_at",
            "location",
            "comments",
            "qr_code",
            "created",
            "modified",
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.generate_qr(self.context["request"])

        return instance


class ConsumableSerializer(MaterialSerializer):
    class Meta(MaterialSerializer.Meta):
        model = Consumable
        fields = MaterialSerializer.Meta.fields + [
            "alert_below",
            "reference",
            "quantity",
            "expiration",
            "warn",
            "relative_percentage",
        ]

    def update(self, instance, validated_data):
        instance.create_log(self.context["request"])

        return super().update(instance, validated_data)

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise ValidationError(
                "A quantidade não pode ser negativa", "negative_quantity"
            )

        return quantity


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class PermanentSerializer(MaterialSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    category = PrimaryKeyRelatedFieldWithSerializer(
        CategorySerializer, queryset=Category.objects.all()
    )

    class Meta(MaterialSerializer.Meta):
        model = Permanent
        fields = MaterialSerializer.Meta.fields + [
            "number",
            "category",
            "status",
            "status_display",
        ]


class HistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = History
        fields = [
            "id",
            "user",
            "quantity",
            "prev_quantity",
            "diff",
            "created",
            "modified",
        ]
