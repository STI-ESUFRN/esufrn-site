from menu.models import Itens
from menu.serializers import ItemSerializer


def menuItens(request):
    itens = Itens.objects.all()
    serializer = ItemSerializer(itens, many=True)
    return {"navbar_items": serializer.data}
