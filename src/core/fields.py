from collections import OrderedDict

from rest_framework import serializers


class PrimaryKeyRelatedFieldWithSerializer(serializers.PrimaryKeyRelatedField):
    def __init__(self, representation_serializer, **kwargs):
        self.representation_serializer = representation_serializer
        super().__init__(**kwargs)

    def to_representation(self, value):
        item = self.queryset.get(pk=value.pk)

        return self.representation_serializer(item).data

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
                        item
                    ),
                    self.display_value(item),
                )
                for item in queryset
            ]
        )
