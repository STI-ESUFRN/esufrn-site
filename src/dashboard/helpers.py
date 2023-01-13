from dashboard.models import DashboardItens
from dashboard.serializers import DashboardItemSerializer


def get_dash_context(context, menuName, current=None):
    try:
        menu = DashboardItens.objects.get(name=menuName)
        serializer = DashboardItemSerializer(menu)
        context["current"] = serializer.data
        if current:
            context["current_sub"] = current
    except DashboardItens.DoesNotExist:
        pass
