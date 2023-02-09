from django.contrib import admin

from dashboard.models import DashboardItens, DashboardSubItens


# Register your models here.
class DashboardSubItensInline(admin.StackedInline):
    model = DashboardSubItens
    extra = 1


class DashboardItensAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    search_fields = ["name", "link"]
    inlines = [
        DashboardSubItensInline,
    ]


admin.site.register(DashboardItens, DashboardItensAdmin)


class DashboardSubItensAdmin(admin.ModelAdmin):
    list_display = ["name", "menu", "link", "order"]
    search_fields = ["name", "link"]
    list_filter = ["menu"]


admin.site.register(DashboardSubItens, DashboardSubItensAdmin)
