from django.contrib import admin

from principal.models import (
    Alert,
    Document,
    File,
    Message,
    News,
    NewsAttachment,
    Newsletter,
    Page,
    Team,
    Testimonial,
)


class BlogAttachmentsInline(admin.TabularInline):
    model = NewsAttachment


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "isImportant",
        "modified_at",
        "published_at",
        "category",
    ]

    search_fields = ["title", "subtitle"]
    list_filter = ["published_at", "author", "category", "isImportant"]
    exclude = ["slug"]
    inlines = [
        BlogAttachmentsInline,
    ]

    @admin.action(description="Adicionar destaque às Notícias selecionadas")
    def add_important(self, request, queryset):
        queryset.update(isImportant=True)

    @admin.action(description="Remover destaque das Notícias selecionadas")
    def remove_important(self, request, queryset):
        queryset.update(isImportant=False)

    actions = [add_important, remove_important]

    class Media:
        js = ("assets/js/jquery-3.3.1.min.js", "assets/js/admin_event.js")


class EquipeAdmin(admin.ModelAdmin):
    list_display = ["name", "sigaa", "kind"]
    search_fields = ["name"]
    list_filter = ["kind"]


class ArquivosAdmin(admin.ModelAdmin):
    list_display = ["name", "file"]
    search_fields = ["name"]


class PaginasAdmin(admin.ModelAdmin):
    list_display = ["name", "path"]
    search_fields = ["name"]


class DepoimentosAdmin(admin.ModelAdmin):
    list_display = ["name", "occupation", "file"]
    search_fields = ["name"]
    list_filter = ["occupation"]


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["name_person", "email", "category", "subscribed_at", "last_updated"]
    search_fields = ["name_person", "email"]
    list_filter = ["category"]


class AdminDocumentos(admin.ModelAdmin):
    list_display = ["name", "category", "document_type", "get_url", "published_at"]
    search_fields = ["name"]
    list_filter = ["category", "document_type"]


class AdminMensagem(admin.ModelAdmin):
    list_display = ["name", "contact"]
    search_fields = ["name", "contact", "message"]


class AdminAlerta(admin.ModelAdmin):
    list_display = ["title", "expires_at", "created", "modified"]
    search_fields = ["title", "content"]


admin.site.register(News)
admin.site.register(Team, EquipeAdmin)
admin.site.register(File, ArquivosAdmin)
admin.site.register(Page, PaginasAdmin)
admin.site.register(Testimonial, DepoimentosAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Document, AdminDocumentos)
admin.site.register(Message, AdminMensagem)
admin.site.register(Alert, AdminAlerta)
