from django.contrib import admin

from revistas.models import Revista


class AdminRevista(admin.ModelAdmin):
    list_display = ["year", "subtitle"]
    search_fields = ["year", "subtitle"]
    list_filter = ["type"]


admin.site.register(Revista, AdminRevista)
