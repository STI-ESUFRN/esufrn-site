from django.contrib import admin

from laboratorio.models import (
    Consumable,
    History,
    Material,
    Permanent,
    UserWarehouse,
    Warehouse,
)


class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    readonly_fields = ["qr_code"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


class ConsumableAdmin(MaterialAdmin):
    list_display = [
        "name",
        "quantity",
    ]
    readonly_fields = ["qr_code"]

    def save_model(self, request, obj, form, change):
        obj.create_log(request)
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


class PermanentAdmin(MaterialAdmin):
    list_display = [
        "name",
        "number",
    ]
    readonly_fields = ["qr_code"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


admin.site.register(Consumable, ConsumableAdmin)
admin.site.register(History)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Permanent, PermanentAdmin)
admin.site.register(UserWarehouse)
admin.site.register(Warehouse)
