from django.contrib import admin
from laboratorio.models import (
    Consumable,
    History,
    Material,
    Permanent,
    UserWarehouse,
    Warehouse,
    Category,
    ConsumableTI,
    HistoryTI,
    MaterialTI,
    PermanentTI,
    WarehouseTI,
    UserWarehouseTI,
    CategoryTI,
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


# Admins para TI
class MaterialTIAdmin(MaterialAdmin):
    list_display = [
        "name",
    ]
    readonly_fields = ["qr_code"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


class ConsumableTIAdmin(ConsumableAdmin):
    list_display = [
        "name",
        "quantity",
    ]
    readonly_fields = ["qr_code"]

    def save_model(self, request, obj, form, change):
        obj.create_log(request)
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


class PermanentTIAdmin(PermanentAdmin):
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
admin.site.register(Category)

# Admins para os modelos TI
admin.site.register(ConsumableTI, ConsumableTIAdmin)
admin.site.register(HistoryTI)
admin.site.register(MaterialTI, MaterialTIAdmin)
admin.site.register(PermanentTI, PermanentTIAdmin)
admin.site.register(WarehouseTI)
admin.site.register(UserWarehouseTI)
admin.site.register(CategoryTI)