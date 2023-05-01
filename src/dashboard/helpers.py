from datetime import time

from django.db.models import Q
from django.utils import timezone

from reserva.models import ReserveDay

MORNING_SHIGT_BEGIN = time(7, 00, 00)
MORNING_SHIGT_END = time(12, 30, 00)
AFTERNOON_SHIFT_BEGIN = time(13, 00, 00)
AFTERNOON_SHIFT_END = time(18, 30, 00)
NIGHT_SHIFT_BEGIN = time(18, 45, 00)
NIGHT_SHIFT_END = time(22, 15, 00)


def get_current_reserves():
    now = timezone.now()
    current_time = timezone.localtime(now).time()

    if MORNING_SHIGT_BEGIN <= current_time <= MORNING_SHIGT_END:
        shift = "M"

    elif AFTERNOON_SHIFT_BEGIN <= current_time <= AFTERNOON_SHIFT_END:
        shift = "T"

    elif NIGHT_SHIFT_BEGIN <= current_time <= NIGHT_SHIFT_END:
        shift = "N"

    else:
        shift = None

    return ReserveDay.objects.filter(
        Q(reserve__status="A") | Q(period__status="A"),
        date=now.date(),
        shift=shift,
    )
