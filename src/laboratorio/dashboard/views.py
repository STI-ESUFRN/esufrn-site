from django.contrib.auth.decorators import login_required
from django.db.models import ExpressionWrapper, F, Sum, fields
from django.http import Http404
from django.shortcuts import redirect, render

from laboratorio.models import Consumable, Permanent
from principal.decorators import allowed_users

material_roles = ["suporte", "material"]


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def home_view(request):
    return redirect("consumable_dashboard")


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def consumable_materials_view(request):
    return render(
        request,
        "laboratorio/dashboard/consumivel/dashboard.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def update_consumable_view(request, pk):
    try:
        item = Consumable.objects.get(id=pk)

    except Consumable.DoesNotExist as err:
        raise Http404(err) from err

    context = {"item": item}
    return render(
        request,
        "laboratorio/dashboard/consumivel/editar.html",
        context,
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_consumable_list_view(request):
    return render(
        request,
        "laboratorio/dashboard/consumivel/relacao.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def permanent_materials_view(request):
    return render(
        request,
        "laboratorio/dashboard/permanente/dashboard.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def update_permanent_view(request, pk):
    try:
        item = Permanent.objects.get(id=pk)

    except Permanent.DoesNotExist as err:
        raise Http404(err) from err

    context = {"item": item}
    return render(
        request,
        "laboratorio/dashboard/permanente/editar.html",
        context,
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def materials_permanent_list_view(request):
    return render(
        request,
        "laboratorio/dashboard/permanente/relacao.html",
    )


@login_required(login_url="/dashboard/login")
@allowed_users(allowed_roles=material_roles)
def report_view(request, year):
    materials = Consumable.objects.all()

    months = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    report = []
    for material in materials:
        material_report = {}
        material_report["name"] = material.name
        material_report["data"] = []

        for month in range(1, 13):
            movements = material.history.filter(
                created__year=year,
                created__month=month,
            ).annotate(
                diff=ExpressionWrapper(
                    F("quantity") - F("prev_quantity"),
                    output_field=fields.IntegerField(),
                ),
            )

            month_report = {}
            month_report["month"] = months[month - 1]
            month_report["highs"] = movements.filter(diff__gt=0).aggregate(
                total_highs=Sum("diff"),
            )["total_highs"]
            month_report["lows"] = movements.filter(diff__lt=0).aggregate(
                total_lows=Sum("diff"),
            )["total_lows"]

            material_report["data"].append(month_report)

        report.append(material_report)

    return render(
        request,
        "laboratorio/dashboard/consumivel/report.html",
        {"report": report, "months": months},
    )
