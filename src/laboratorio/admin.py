from django.contrib import admin

from laboratorio.models import History, Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "quantity",
        "number",
    ]
    readonly_fields = ["qr"]

    def save_model(self, request, obj, form, change):
        obj.create_log(request)
        super().save_model(request, obj, form, change)
        obj.generate_qr(request)


admin.site.register(Material, MaterialAdmin)
admin.site.register(History)
