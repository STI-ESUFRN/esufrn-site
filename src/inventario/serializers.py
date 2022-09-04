from rest_framework import serializers

from .models import *


class PatrimonioSerializador(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.get_category()

    class Meta:
        model = Patrimonio
        fields = "__all__"


class EmprestimoSerializador(serializers.ModelSerializer):

    borrow_date = serializers.DateTimeField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "iso-8601"]
    )
    return_date = serializers.DateTimeField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "iso-8601"]
    )

    class Meta:
        model = Emprestimo
        fields = "__all__"


class MaquinaSerializador(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = "__all__"


class PedidosSerializador(serializers.ModelSerializer):
    patrimony = PatrimonioSerializador(read_only=False)

    class Meta:
        model = PatrimonioEmprestimo
        fields = ("patrimony", "quantity")
