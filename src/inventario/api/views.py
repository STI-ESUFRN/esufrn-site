from django.http import JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views.generic import View

from inventario.models import Emprestimo, Maquina, Patrimonio, PatrimonioEmprestimo
from inventario.serializers import (
    EmprestimoSerializer,
    MaquinaSerializer,
    PatrimonioSerializer,
    PedidosSerializer,
)
from principal.decorators import allowed_users
from principal.utils import paginate

decorators = [
    allowed_users(allowed_roles=["suporte"]),
]


@method_decorator(decorators, name="dispatch")
class patrimoniosView(View):
    def get(self, request, *args, **kwargs):
        patrimonios = Patrimonio.objects.all()
        serializer = PatrimonioSerializer(patrimonios, many=True)

        return JsonResponse(serializer.data, safe=False)


@method_decorator(decorators, name="dispatch")
class emprestimosView(View):
    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", "1"))

        npp = 8
        paginatorJSON = {"current": page, "total": 0, "npp": npp}

        emprestimos = Emprestimo.objects.all()

        status = request.GET.get("status")
        if status:
            emprestimos = emprestimos.filter(status=status)

        serializador = EmprestimoSerializer(paginate(emprestimos, page, npp), many=True)

        paginatorJSON["total"] = int(emprestimos.count() / npp) + 1

        return JsonResponse(
            {"data": serializador.data, "paginator": paginatorJSON}, safe=False
        )


@method_decorator(decorators, name="dispatch")
class emprestimoView(View):
    def get(self, request, *args, **kwargs):
        emprestimo = Emprestimo.objects.get(id=kwargs["pk"])
        serializer = EmprestimoSerializer(emprestimo, many=False)

        return JsonResponse(serializer.data, safe=False)

    def put(self, request, *args, **kwargs):
        PUT = QueryDict(request.body)

        try:
            emprestimo = Emprestimo.objects.get(id=kwargs["pk"])
            status = PUT.get("status")
            if status is not None:
                emprestimo.update(status=status)

            return JsonResponse(
                {"status": "success", "message": "Arquivo atualizado com sucesso"},
                safe=False,
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "{}".format(next(iter(e)))}, safe=False
            )


@method_decorator(decorators, name="dispatch")
class emprestimoPatrimoniosView(View):
    def get(self, request, *args, **kwargs):
        emprestimo = Emprestimo.objects.get(id=kwargs["pk"])
        pe = PatrimonioEmprestimo.objects.filter(loan=emprestimo)

        serializer = PedidosSerializer(pe, many=True)

        return JsonResponse(serializer.data, safe=False)


@method_decorator(decorators, name="dispatch")
class maquinasView(View):
    def get(self, request, *args, **kwargs):
        maquinas = Maquina.objects.all()
        serializer = MaquinaSerializer(maquinas, many=True)

        return JsonResponse(serializer.data, safe=False)
