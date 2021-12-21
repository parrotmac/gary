from django import template

register = template.Library()


def has_intersection(a: list, b: list):
    return bool(set(a) & set(b))


register.filter('has_intersection', has_intersection)
