import hashlib

from django import template

register = template.Library()


@register.filter(name="md5")
def md5_string(value):
    return hashlib.md5(value.encode("utf-8")).hexdigest()


@register.filter(name="has_intersection")
def has_intersection(a: list, b: list):
    return bool(set(a) & set(b))
