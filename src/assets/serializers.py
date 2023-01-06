from rest_framework import serializers

from assets.models import ESImage, File


class ESImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESImage
        fields = [
            "high",
            "medium",
            "low",
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "url",
        ]
