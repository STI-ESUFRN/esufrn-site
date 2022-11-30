from dashboard.models import DashboardItens
from dashboard.serializers import DashboardItemSerializer


def dashboardMenuItens(request):
    items = DashboardItens.objects.all()
    serializer = DashboardItemSerializer(items, many=True)

    return {"dashboard_navbar_items": serializer.data}
