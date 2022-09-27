from django.contrib import admin

from menu.models import Itens, SubItens, SubSubItens

# Register your models here.


class ItensAdmin(admin.ModelAdmin):
    list_display = ["name", "action_type", "get_link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["action_type"]


admin.site.register(Itens, ItensAdmin)


class SubItensAdmin(admin.ModelAdmin):
    list_display = ["name", "menu", "action_type", "get_link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["menu", "action_type"]


admin.site.register(SubItens, SubItensAdmin)


class SubSubItensAdmin(admin.ModelAdmin):
    list_display = ["name", "submenu", "link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["submenu"]


admin.site.register(SubSubItens, SubSubItensAdmin)
