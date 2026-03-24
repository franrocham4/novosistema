from django import template

register = template.Library()


@register.filter
def brl(value):
    """Format a number using the Brazilian monetary format: 1.234.567,89"""
    try:
        val = float(value)
    except (TypeError, ValueError):
        return value
    formatted = '{:,.2f}'.format(val)
    # Swap separators: 1,234,567.89 -> 1.234.567,89
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted
