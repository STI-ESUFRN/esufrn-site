from datetime import timedelta

from django.apps import apps
from django.db import models, transaction
from rest_framework.exceptions import ValidationError


class ReserveManager(models.Manager):
    @transaction.atomic
    def create(self, **kwargs):
        instance = super().create(**kwargs)

        reserve_day_model_cls = apps.get_model("reserva", "ReserveDay")
        reserve_day_model_cls.objects.create(
            reserve=instance,
            date=instance.date,
            shift=instance.shift,
            classroom=instance.classroom,
        )

        return instance


class PeriodManager(models.Manager):
    @transaction.atomic
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        self.ensure_days(instance)
        return instance

    @classmethod
    @transaction.atomic
    def ensure_days(cls, instance):
        reserve_day_model_cls = apps.get_model("reserva", "ReserveDay")
        instance.days.all().delete()
        current_date = instance.date_begin

        invalid_dates = []
        while current_date <= instance.date_end:
            if str(current_date.isoweekday()) in instance.weekdays:
                for shift in instance.shift:
                    try:
                        reserve_day_model_cls.objects.create(
                            period=instance,
                            date=current_date,
                            shift=shift,
                            classroom=instance.classroom,
                        )

                    except ValidationError:
                        invalid_dates.append({"date": current_date, "shift": shift})

            current_date += timedelta(days=1)

        if invalid_dates:
            days = ", ".join(
                [f"{day['date']} ({day['shift']})" for day in invalid_dates]
            )
            raise ValidationError(
                {
                    "non_fields_error": [
                        f"Já existem reservas aprovadas para os dias {days}."
                    ]
                }
            )
