from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

MINIMUM_ALLOWED_YEAR = 1984


def year_validator(year):
    if year < MINIMUM_ALLOWED_YEAR or year > timezone.now().year:
        raise ValidationError(_("Invalid year"))
