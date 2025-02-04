from django.urls import path

from laboratorio.dashboard.views import (
    consumable_materials_view,
    home_view,
    materials_consumable_list_view,
    materials_permanent_list_view,
    permanent_materials_view,
    report_view,
    reports_view,
    update_consumable_view,
    update_permanent_view,
    #-----
    consumable_ti_materials_view,
    permanent_ti_materials_view,
    materials_consumable_ti_list_view,
    materials_permanent_ti_list_view,
    report_ti_view,
    reports_ti_view,
    update_consumable_ti_view,
    update_permanent_ti_view,
)

urlpatterns = [
    path("", home_view),
    path("consumivel/", consumable_materials_view, name="consumable_dashboard"),
    path("consumivel/<int:pk>/", update_consumable_view, name="update_consumable"),
    path("consumivel/relacao/", materials_consumable_list_view, name="consumable_list"),
    path("consumivel/relatorio/<int:year>/", report_view, name="consumable_report"),
    path("consumivel/relatorio/", reports_view, name="report_list"),
    path("permanente/", permanent_materials_view, name="permanent_dashboard"),
    path("permanente/<int:pk>/", update_permanent_view, name="update_permanent"),
    path("permanente/relacao/", materials_permanent_list_view, name="permanent_list"),
    #------
    path("consumivel_ti/", consumable_ti_materials_view, name="consumable_ti_dashboard"),
    path("consumivel_ti/<int:pk>/", update_consumable_ti_view, name="update_consumable_ti"),
    path("consumivel_ti/relacao/", materials_consumable_ti_list_view, name="consumable_ti_list"),
    path("consumivel_ti/relatorio/<int:year>/", report_ti_view, name="consumable_ti_report"),
    path("consumivel_ti/relatorio/", reports_ti_view, name="report_ti_list"),
    path("permanente_ti/", permanent_ti_materials_view, name="permanent_ti_dashboard"),
    path("permanente_ti/<int:pk>/", update_permanent_ti_view, name="update_permanent_ti"),
    path("permanente_ti/relacao/", materials_permanent_ti_list_view, name="permanent_ti_list"),
]