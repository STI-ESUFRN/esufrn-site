from collections import OrderedDict

from rest_framework import serializers


class MultiSelectField(serializers.ChoiceField):
    def to_internal_value(self, data):
        return data.split(",")

    def to_representation(self, value):
        return value


class PrimaryKeyRelatedFieldWithSerializer(serializers.PrimaryKeyRelatedField):
    def __init__(self, representation_serializer, **kwargs):
        self.representation_serializer = representation_serializer
        super().__init__(**kwargs)

    def to_representation(self, value):
        instance = self.queryset.get(pk=value.pk)

        return self.representation_serializer(instance, context=self.context).data

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict(
            [
                (
                    super(PrimaryKeyRelatedFieldWithSerializer, self).to_representation(
                        item,
                    ),
                    self.display_value(item),
                )
                for item in queryset
            ],
        )
