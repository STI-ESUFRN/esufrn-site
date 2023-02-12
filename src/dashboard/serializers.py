from rest_framework import serializers

from dashboard.models import DashboardItens, DashboardSubItens


class DashboardSubitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardSubItens
        fields = [
            "id",
            "name",
            "related_name",
            "link",
            "order",
            "menu",
            "decoration",
            "aditional",
        ]


class DashboardItemSerializer(serializers.ModelSerializer):
    subitems = DashboardSubitemSerializer(many=True)

    class Meta:
        model = DashboardItens
        fields = [
            "id",
            "name",
            "subitems",
            "link",
            "order",
            "decoration",
        ]
