from django import forms
from django.contrib import admin

from reserva.models import Classroom, Period, Reserve, ReserveDay, UserClassroom

# Register your models here.


class UserClassroomInline(admin.TabularInline):
    model = UserClassroom


class AdminClassroom(admin.ModelAdmin):
    list_display = ["number", "name", "type", "days_required", "justification_required"]
    list_filter = ["type", "floor", "days_required", "justification_required"]
    inlines = [
        UserClassroomInline,
    ]


class AdminUserClassroom(admin.ModelAdmin):
    list_display = ["user", "get_user_email", "classroom"]
    list_filter = ["user", "classroom"]


class AdminReserve(admin.ModelAdmin):
    list_display = [
        "classroom",
        "date",
        "shift",
        "requester",
        "email",
        "status",
    ]
    exclude = ["tag"]
    search_fields = [
        "event",
        "equipment",
        "email",
        "phone",
        "obs",
    ]
    list_filter = ["status", "classroom", "shift", "date"]


class PeriodAdminForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove sábado (6) e domingo (7) das opções de dias da semana
        if 'weekdays' in self.fields:
            choices = [choice for choice in self.fields['weekdays'].choices 
                      if choice[0] not in ['6', '7']]
            self.fields['weekdays'].choices = choices


class AdminPeriodReserve(admin.ModelAdmin):
    form = PeriodAdminForm
    list_display = [
        "classname",
        "course",
        "period",
        "class_period",
        "date_begin",
        "date_end",
        "shift",
        "requester",
        "email",
        "status",
    ]
    search_fields = [
        "classname",
        "course",
        "requester",
        "email",
        "phone",
    ]
    list_filter = ["course", "classroom", "requester", "status"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "classname",
                    "course",
                    "classcode",
                    "classroom",
                    "date_begin",
                    "date_end",
                    "workload",
                    "period",
                    "class_period",
                    "weekdays",
                    "shift",
                    "equipment",
                ),
            },
        ),
        ("Dados do docente", {"fields": ("requester", "email", "phone")}),
        ("Administração", {"fields": ("status",)}),
    )


class AdminReserveDay(admin.ModelAdmin):
    list_display = ["date", "shift"]
    search_fields = ["date"]
    list_filter = ["shift"]
    readonly_fields = ["date"]


admin.site.register(Reserve, AdminReserve)
admin.site.register(Classroom, AdminClassroom)
admin.site.register(UserClassroom, AdminUserClassroom)
admin.site.register(Period, AdminPeriodReserve)
admin.site.register(ReserveDay, AdminReserveDay)
