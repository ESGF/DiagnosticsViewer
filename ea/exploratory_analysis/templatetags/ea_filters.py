from django import template

register = template.Library()


@register.filter
def get(l, index):
    return l[index]

