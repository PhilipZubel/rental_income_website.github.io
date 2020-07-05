from django import template

register = template.Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_value_by_index(l, index):
    return l[index]

