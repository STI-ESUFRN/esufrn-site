from django import template
from django.conf import settings
import re
from django.utils.translation import gettext_lazy as _

register = template.Library()


def bold(str):
    pattern = re.compile(
        '|'.join((re.escape(word) for word in settings.BOLD.split())), re.I
    )
    result = re.sub(pattern, r'<b>\g<0></b>', str)

    return result


register.filter('bold', bold)


def mark(str):
    result = re.sub('', r'', str)
    if settings.BOLD != '':
        pattern = re.compile(re.escape(settings.BOLD), re.I)
        result = re.sub(pattern, r'<mark>\g<0></mark>', str)

    return result


register.filter('mark', mark)


def split(value, key):
    return value.split(key)


register.filter('split', split)


def enum(value, key):
    list = value.split(key)
    length = len(list)

    if length > 2:
        return "{} {} {}".format(", ".join(list[0:length-1]), _("and"), list[length-1])

    elif length > 1:
        return " {} ".format(_("and")).join(list)

    else:
        return value


register.filter('enum', enum)


def active(value, target=""):
    if value == target:
        return "active"

    return ""


register.filter('active', active)


def getparam(value, key):
    if value:
        return "&{}={}".format(key, value)

    return ""


register.filter('getparam', getparam)
