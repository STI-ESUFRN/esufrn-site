from django.db.models import BooleanField, Case, When

from dashboard.models import DashboardItens, DashboardSubItens


def navbar(request):
    context = {}
    current_menu = None

    subitem = DashboardSubItens.objects.filter(link=request.path).first()
    if subitem:
        current_menu = subitem.menu

    if not current_menu:
        item = DashboardItens.objects.filter(link=request.path).first()
        if item:
            current_menu = item

    if current_menu:
        items = (
            DashboardItens.objects.all()
            .values("name", "link")
            .annotate(
                is_active=Case(
                    When(id=current_menu.id, then=True),
                    default=False,
                    output_field=BooleanField(),
                )
            )
        )

        subitems = (
            DashboardSubItens.objects.filter(menu=current_menu)
            .values("name", "link")
            .annotate(
                is_active=Case(
                    When(link=request.path, then=True),
                    default=False,
                    output_field=BooleanField(),
                )
            )
        )

        context = {
            "dashboard_navbar_items": items,
            "dashboard_navbar_subitems": subitems,
        }

    else:
        items = DashboardItens.objects.all().values("name", "link")
        context = {
            "dashboard_navbar_items": items,
        }

    return context
