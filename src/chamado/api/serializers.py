from rest_framework import serializers

from chamado.models import *


class ChamadoSerializador(serializers.ModelSerializer):

    class Meta:
        model = Chamado
        fields = ['title', 'description', 'requester', 'course', 'contact']


class ChamadoAdminSerializador(serializers.ModelSerializer):

    class Meta:
        model = Chamado
        exclude = ["solved_at"]
