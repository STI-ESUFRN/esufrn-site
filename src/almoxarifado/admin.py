from django.contrib import admin

from almoxarifado.models import Material, MaterialInstance


class MaterialInstanceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "expiration",
        "quantity",
    ]
    search_fields = ["name"]
    readonly_fields = ["qr"]

    def save_model(self, request, obj, form, change) -> None:
        obj.generate_qr(request)
        return super().save_model(request, obj, form, change)


admin.site.register(MaterialInstance, MaterialInstanceAdmin)
admin.site.register(Material)
