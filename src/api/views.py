
from chamado.api.serializers import ChamadoSerializador
from chamado.models import Chamado
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import View
from principal.decorators import allowed_users
from principal.models import Mensagem
from reserva.models import Reserve
from reserva.serializers import ReserveSerializador


@allowed_users(allowed_roles=['suporte'])
@require_GET
def search(request):
    result = Chamado.objects.filter(Q(name__icontains=request.GET['search']) | Q(
        obs__icontains=request.GET['search'])).exclude(status__isnull=True)
    resultRes = Reserve.objects.filter(Q(classroom__classroom__icontains=request.GET['search']) | Q(event__icontains=request.GET['search']) | Q(
        requester__icontains=request.GET['search']) | Q(obs__icontains=request.GET['search'])).exclude(status='E')

    merge = []

    serializador = ChamadoSerializador(result, many=True)
    merge += serializador.data
    serializador = ReserveSerializador(resultRes, many=True)
    merge += serializador.data

    return JsonResponse(merge, safe=False)


class contatosView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("nome")
        contact = request.POST.get("contato")
        message = request.POST.get("mensagem")

        try:
            Mensagem.objects.create(
                name=name,
                contact=contact,
                message=message
            )

            return JsonResponse({"status": "success", "message": "Mensagem enviada com sucesso."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": "{}".format(next(iter(e)))})


decorators = [
    allowed_users(allowed_roles=['suporte']),
]


@method_decorator(decorators, name="dispatch")
class contatoView(View):
    def delete(self, request, *args, **kwargs):
        try:
            Mensagem.objects.get(id=self.kwargs['pk']).delete()
            return JsonResponse({"message": "Arquivo excluído com sucesso", "status": "success"})

        except Exception as e:
            return JsonResponse({"message": e, "status": "error"})
