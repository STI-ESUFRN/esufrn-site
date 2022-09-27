from django.contrib import admin

from chamado.models import Chamado


class AdminCall(admin.ModelAdmin):
    list_display = ["title", "requester", "status", "course", "contact"]
    search_fields = ["title", "requester"]
    list_filter = ["status"]


admin.site.register(Chamado, AdminCall)
