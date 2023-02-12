from django.db import models
from django.utils.translation import gettext as _

DAY_OF_THE_WEEK = {
    "1": _("Monday"),
    "2": _("Tuesday"),
    "3": _("Wednesday"),
    "4": _("Thursday"),
    "5": _("Friday"),
    "6": _("Saturday"),
    "7": _("Sunday"),
}


class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs["max_length"] = 1
        super().__init__(*args, **kwargs)
