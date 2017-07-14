import datetime

from django import template

register = template.Library()


@register.simple_tag
def row_class(ap, my_aps):
    if ap.strip() in my_aps:
        return "table-danger"
    else:
        return None
