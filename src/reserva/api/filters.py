from django.utils import timezone
from django_filters import FilterSet

from reserva.models import ReserveDay


class CalendarFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        kwargs["data"]._mutable = True
        now = timezone.now()
        kwargs["data"].setdefault("date__month", now.month)
        kwargs["data"].setdefault("date__year", now.year)

        kwargs["data"]._mutable = False
        super().__init__(*args, **kwargs)

    class Meta:
        model = ReserveDay
        fields = {
            "classroom": ["exact"],
            "date": ["exact", "month", "year"],
        }
