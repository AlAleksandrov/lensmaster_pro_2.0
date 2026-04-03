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

@register.simple_tag(takes_context=True)
def can_manage(context, obj=None):
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    if request.user.is_superuser or request.user.is_staff:
        return True
    return request.user.groups.filter(name='Photographers').exists()