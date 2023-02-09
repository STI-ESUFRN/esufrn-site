import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def year_validator(year):
    if year < 1984 or year > datetime.date.today().year:
        raise ValidationError(_("Invalid year"))
