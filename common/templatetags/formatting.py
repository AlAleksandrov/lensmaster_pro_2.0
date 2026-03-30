from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='eur')
def eur(value):

    if value is None or value == '':
        return '€0.00'

    try:
        dec = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return f'€{value}'

    return f'€{dec:.2f}'

@register.filter(name='hours_label')
def hours_label(value):
    try:
        hours = int(value)
    except (TypeError, ValueError):
        return f"{value}h"
    if hours == 1:
        return '1 hour'
    return f'{hours} hours'

@register.simple_tag
def featured_badge(is_featured):
    if is_featured:
        return '⭐ Featured'
    return ''
