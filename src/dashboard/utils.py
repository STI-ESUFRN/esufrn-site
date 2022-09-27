from .models import DashboardItens, DashboardSubItens


def getDashContext(context, menuName, current=None):
    menu = DashboardItens.objects.get(name=menuName)
    context["current"] = {
        "main": menu,
        "subs": DashboardSubItens.objects.all().filter(menu=menu.id),
    }
    if current:
        context["current_sub"] = current
