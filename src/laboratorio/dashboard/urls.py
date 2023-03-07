from django.urls import path

from laboratorio.dashboard.views import (
    consumable_materials_view,
    home_view,
    materials_consumable_list_view,
    materials_permanent_list_view,
    permanent_materials_view,
    update_consumable_view,
    update_permanent_view,
)

urlpatterns = [
    path("", home_view),
    path("consumivel/", consumable_materials_view, name="consumable_dashboard"),
    path("consumivel/<int:pk>/", update_consumable_view, name="update_consumable"),
    path("consumivel/relacao/", materials_consumable_list_view, name="consumable_list"),
    path("permanente/", permanent_materials_view, name="permanent_dashboard"),
    path("permanente/<int:pk>/", update_permanent_view, name="update_permanent"),
    path("permanente/relacao/", materials_permanent_list_view, name="permanent_list"),
]
