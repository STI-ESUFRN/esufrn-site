import re

from django import template
from django.conf import settings
from django.utils.translation import gettext as _

register = template.Library()


def bold(str):
    pattern = re.compile(
        "|".join((re.escape(word) for word in settings.BOLD.split())),
        re.I,
    )

    return re.sub(pattern, r"<b>\g<0></b>", str)


def mark(str):
    result = re.sub("", r"", str)
    if settings.BOLD:
        pattern = re.compile(re.escape(settings.BOLD), re.I)
        result = re.sub(pattern, r"<mark>\g<0></mark>", str)

    return result


def split(value, key):
    return value.split(key)


def enum(value, key):
    list = value.split(key)
    length = len(list)

    if length > 2:
        return "{} {} {}".format(
            ", ".join(list[0 : length - 1]),
            _("and"),
            list[length - 1],
        )

    if length > 1:
        return " {} ".format(_("and")).join(list)

    return value


def active(value, target=""):
    if value == target:
        return "active"

    return ""


def getparam(value, key):
    if value:
        return "&{}={}".format(key, value)

    return ""


register.filter("bold", bold)
register.filter("mark", mark)
register.filter("split", split)
register.filter("enum", enum)
register.filter("active", active)
register.filter("getparam", getparam)
