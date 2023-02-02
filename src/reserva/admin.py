from django.contrib import admin

from reserva.models import (
    Classroom,
    PeriodReserve,
    PeriodReserveDay,
    Reserve,
    UserClassroom,
)

# Register your models here.


class UserClassroomInline(admin.TabularInline):
    model = UserClassroom


class AdminClassroom(admin.ModelAdmin):
    list_display = ["number", "name", "type", "days_required", "justification_required"]
    list_filter = ["type", "floor", "days_required", "justification_required"]
    inlines = [
        UserClassroomInline,
    ]


admin.site.register(Classroom, AdminClassroom)


class AdminUserClassroom(admin.ModelAdmin):
    list_display = ["user", "get_user_email", "classroom"]
    list_filter = ["user", "classroom"]


admin.site.register(UserClassroom, AdminUserClassroom)


class AdminReserve(admin.ModelAdmin):
    list_display = [
        "classroom",
        "date",
        "shift",
        # "equipment",
        "requester",
        "email",
        "status",
        # "event",
        # "phone",
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

    def save_model(self, request, obj, form, change):
        if "status" in form.changed_data:
            if obj.status is not None:
                obj.notify()

        super().save_model(request, obj, form, change)


admin.site.register(Reserve, AdminReserve)


class AdminPeriodReserve(admin.ModelAdmin):
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
                )
            },
        ),
        ("Dados do docente", {"fields": ("requester", "email", "phone")}),
        ("Administração", {"fields": ("status",)}),
    )


admin.site.register(PeriodReserve, AdminPeriodReserve)


class AdminPeriodReserveDay(admin.ModelAdmin):
    list_display = ["get_period_classroom", "date", "get_period_requester", "shift"]
    search_fields = ["period", "date"]
    list_filter = ["period", "period__requester", "period__classroom", "shift"]
    readonly_fields = ["period", "date"]


admin.site.register(PeriodReserveDay, AdminPeriodReserveDay)
