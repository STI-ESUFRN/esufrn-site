from django.contrib import admin

from eventos.models import AdditionalInformation, Attachment, Event


class AdditionalInformationInline(admin.TabularInline):
    model = AdditionalInformation
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = Attachment


class EventAdmin(admin.ModelAdmin):
    display_fields = ["id", "name", "date_begin", "date_end"]
    prepopulated_fields = {"slug": ["name", "date_begin"]}
    inlines = [
        AdditionalInformationInline,
        AttachmentInline,
    ]


class AdditionalInformationAdmin(admin.ModelAdmin):
    display_fields = ["id", "name", "event"]


class AttachmentAdmin(admin.ModelAdmin):
    display_fields = ["id", "event", "file"]


admin.site.register(Event, EventAdmin)
admin.site.register(AdditionalInformation, AdditionalInformationAdmin)
admin.site.register(Attachment, AttachmentAdmin)
