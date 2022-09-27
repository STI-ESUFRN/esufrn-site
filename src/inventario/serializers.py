from rest_framework import serializers

from inventario.models import Emprestimo, Maquina, Patrimonio, PatrimonioEmprestimo


class PatrimonioSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.get_category()

    class Meta:
        model = Patrimonio
        fields = "__all__"


class EmprestimoSerializer(serializers.ModelSerializer):
    borrow_date = serializers.DateTimeField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "iso-8601"]
    )
    return_date = serializers.DateTimeField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "iso-8601"]
    )

    class Meta:
        model = Emprestimo
        fields = "__all__"


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = "__all__"


class PedidosSerializer(serializers.ModelSerializer):
    patrimony = PatrimonioSerializer(read_only=False)

    class Meta:
        model = PatrimonioEmprestimo
        fields = ("patrimony", "quantity")
