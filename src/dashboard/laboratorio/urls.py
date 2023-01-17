from django.urls import path

from dashboard.laboratorio.views import (
    consumable_materials_view,
    create_consumable_material_view,
    create_permanent_material_view,
    materials_list_view,
    permanent_materials_view,
    update_consumable_view,
    update_permanent_view,
)

urlpatterns = [
    path("consumivel/", consumable_materials_view),
    path(
        "consumivel/inserir/",
        create_consumable_material_view,
        name="material_consumivel_inserir",
    ),
    path("consumivel/<int:pk>/", update_consumable_view, name="consumivel_editar"),
    path("permanente/", permanent_materials_view),
    path(
        "permanente/inserir/",
        create_permanent_material_view,
        name="material_permanente_inserir",
    ),
    path("permanente/<int:pk>/", update_permanent_view, name="permanente_editar"),
    path("relacao/", materials_list_view),
]
