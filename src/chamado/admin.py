from django.contrib import admin

from chamado.models import Chamado, Sala


class AdminSala(admin.ModelAdmin):
    list_display = ["nome"]
    search_fields = ["nome"]


class AdminCall(admin.ModelAdmin):
    list_display = ["equipment", "tombamento", "requester", "status", "room_display"]
    search_fields = ["equipment", "tombamento", "requester", "sala__nome", "sala_outros"]
    list_filter = ["status"]

    def room_display(self, obj):
        return obj.get_room_display()

    room_display.short_description = "Sala"


admin.site.register(Sala, AdminSala)
admin.site.register(Chamado, AdminCall)
