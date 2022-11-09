from django.contrib import admin

from eventos.models import AdditionalInformation, Attachment, Event


class AdditionalInformationInline(admin.TabularInline):
    model = AdditionalInformation
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = Attachment


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "date_begin", "date_end"]
    inlines = [
        AdditionalInformationInline,
        AttachmentInline,
    ]
    exclude = ["slug"]


class AdditionalInformationAdmin(admin.ModelAdmin):
    list_display = ["name", "event"]


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["event", "url"]


admin.site.register(Event, EventAdmin)
admin.site.register(AdditionalInformation, AdditionalInformationAdmin)
admin.site.register(Attachment, AttachmentAdmin)
