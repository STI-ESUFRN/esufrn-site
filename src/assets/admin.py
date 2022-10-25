from django.contrib import admin

from assets.models import ESImage, File


class ESImageAdmin(admin.ModelAdmin):
    search_fields = ["id"]


class FileAdmin(admin.ModelAdmin):
    search_fields = ["id"]


admin.site.register(ESImage, ESImageAdmin)
admin.site.register(File, FileAdmin)
