from django.contrib import admin
from django.utils.html import format_html

from assets.models import ESImage, File


class ESImageAdmin(admin.ModelAdmin):
    list_display = ["image_tag", "high"]
    search_fields = ["high"]
    readonly_fields = ["medium", "low", "image_tag"]

    def image_tag(self, obj):
        return format_html(f"<img style='width:25%;' src='{obj.high.url}'/>")


class FileAdmin(admin.ModelAdmin):
    search_fields = ["id"]


admin.site.register(ESImage, ESImageAdmin)
admin.site.register(File, FileAdmin)
