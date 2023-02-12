from django.contrib import admin

from menu.models import Itens, SubItens


class ItensAdmin(admin.ModelAdmin):
    list_display = ["name", "action_type", "get_link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["action_type"]


class SubItensAdmin(admin.ModelAdmin):
    list_display = ["name", "menu", "link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["menu"]


admin.site.register(Itens, ItensAdmin)
admin.site.register(SubItens, SubItensAdmin)
