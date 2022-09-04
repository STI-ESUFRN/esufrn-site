from .models import *


def dashboardMenuItens(request):
    mainItens = DashboardItens.objects.all()
    mainList = []
    for item in mainItens:
        sub = DashboardSubItens.objects.all().filter(menu=item.id)
        mainList.append({
            "main": item,
            "subs": sub
        })

    return {"dashbordItens": mainList}
