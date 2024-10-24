from django.contrib import admin
from django.utils.translation import gettext as _

from principal.models import (
    Alert,
    Document,
    File,
    Message,
    News,
    NewsAttachment,
    Newsletter,
    Page,
    Photo,
    Team,
    Testimonial,
    Links_V,
    destaque,
    Noticia,
    Cursos_Pronatec,
)


class BlogAttachmentsInline(admin.TabularInline):
    model = NewsAttachment


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "is_important",
        "modified",
        "created",
        "category",
    ]
    readonly_fields = ["created", "modified", "published_at"]

    search_fields = ["title", "subtitle"]
    list_filter = ["created", "author", "category", "is_important"]
    fieldsets = [
        (
            None,
            {"fields": ["title", "subtitle", "author"]},
        ),
        (
            _("News"),
            {"fields": ["image", "news"]},
        ),
        (
            _("Options"),
            {"fields": ["category", "is_important", "published", "publish_in"]},
        ),
        (
            _("Impotant Dates"),
            {"fields": ["published_at", "created", "modified"]},
        ),
    ]
    inlines = [
        BlogAttachmentsInline,
    ]

    @admin.action(description="Adicionar destaque às Notícias selecionadas")
    def add_important(self, request, queryset):
        queryset.update(is_important=True)

    @admin.action(description="Remover destaque das Notícias selecionadas")
    def remove_important(self, request, queryset):
        queryset.update(is_important=False)

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
    list_display = [
        "name",
        "is_active",
        "category",
        "document_type",
        "get_url",
        "created",
    ]
    search_fields = ["name"]
    list_filter = ["category", "document_type"]

    fieldsets = [
        (None, {
            'fields': ('name', 'authors', 'category', 'ensino_subcategory', 'document_type', 'file', 'link', 'date', 'is_active')
        }),
    ]

    class Media:
        js = ("assets/js/admin_documents.js",)



class AdminMensagem(admin.ModelAdmin):
    list_display = ["name", "contact"]
    search_fields = ["name", "contact", "message"]


class AdminAlerta(admin.ModelAdmin):
    list_display = ["title", "expires_at", "created", "modified"]
    search_fields = ["title", "content"]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "image")  # Renomeie de 'caption' para 'descricao'

    def descricao(self, obj):
        return obj.descricao

    descricao.short_description = "Descrição"


class Links_VAdmin(admin.ModelAdmin):
    list_display = ("titulo", "imagem", "link")


class DestaqueAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "imagem", "video_file", "link")

class CursosPronatecAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'imagem', 'link')

admin.site.register(Noticia)
admin.site.register(News, BlogAdmin)
admin.site.register(Team, EquipeAdmin)
admin.site.register(File, ArquivosAdmin)
admin.site.register(Page, PaginasAdmin)
admin.site.register(Testimonial, DepoimentosAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Document, AdminDocumentos)
admin.site.register(Message, AdminMensagem)
admin.site.register(Alert, AdminAlerta)
admin.site.register(Links_V, Links_VAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(destaque, DestaqueAdmin)
admin.site.register(Cursos_Pronatec, CursosPronatecAdmin)
