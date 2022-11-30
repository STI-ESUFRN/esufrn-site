from rest_framework import serializers


class PrimaryKeyRelatedFieldWithSerializer(serializers.PrimaryKeyRelatedField):
    def __init__(self, representation_serializer, **kwargs):
        self.representation_serializer = representation_serializer
        super().__init__(**kwargs)

    def to_representation(self, value):
        instance = self.queryset.get(pk=value.pk)

        return self.representation_serializer(instance).data
