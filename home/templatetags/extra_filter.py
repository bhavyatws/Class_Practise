from atexit import register
from django import template
register=template.Library()
@register.filter(name='get_value')#namig this filter as get_value and writings its function
#this function return dictionary key
def get_value(dict,key):
    return dict.get(key)


