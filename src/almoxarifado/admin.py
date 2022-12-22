from django.contrib import admin

from almoxarifado.models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "expiration",
        "quantity",
    ]
    search_fields = ["name"]
    readonly_fields = ["qr"]


admin.site.register(Material, MaterialAdmin)
