from django.contrib import admin

from .models import Emprestimo, Maquina, Patrimonio, PatrimonioEmprestimo

# Register your models here.


class PatrimonioInline(admin.TabularInline):
    model = PatrimonioEmprestimo

    def has_change_permission(self, request, obj=None):
        return False if obj else True

    def has_delete_permission(self, request, obj=None):
        return False if obj else True


class AdminEmprestimo(admin.ModelAdmin):
    list_display = ["name", "classroom", "borrow_date", "return_date"]
    inlines = [
        PatrimonioInline,
    ]


admin.site.register(Emprestimo, AdminEmprestimo)


class AdminMaquina(admin.ModelAdmin):
    list_display = [
        "get_model",
        "get_dmp",
        "ram",
        "hdd",
        "status",
    ]
    search_fields = ["patrimony__model", "patrimony__dmp", "status"]
    list_filter = ["patrimony__model",
                   "patrimony__dmp", "ram", "hdd", "patrimony__last_updated"]


admin.site.register(Maquina, AdminMaquina)


class AdminPatrimonio(admin.ModelAdmin):
    list_display = [
        "model",
        "dmp",
        "category",
        "status",
        "last_updated",
    ]
    search_fields = ["model", "dmp", "category"]
    list_filter = ["model", "dmp", "category", "last_updated"]


admin.site.register(Patrimonio, AdminPatrimonio)


class AdminPatrimonioEmprestimo(admin.ModelAdmin):
    list_display = ["patrimony", "loan"]
    search_fields = ["patrimony", "loan"]
    list_filter = ["patrimony"]


admin.site.register(PatrimonioEmprestimo, AdminPatrimonioEmprestimo)
