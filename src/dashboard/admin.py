from django.contrib import admin

from .models import *

# Register your models here.


class DashboardItensAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    search_fields = ["name", "link"]


admin.site.register(DashboardItens, DashboardItensAdmin)


class DashboardSubItensAdmin(admin.ModelAdmin):
    list_display = ["name", "menu", "link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["menu"]


admin.site.register(DashboardSubItens, DashboardSubItensAdmin)
