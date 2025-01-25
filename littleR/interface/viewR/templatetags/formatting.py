from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def title_string(value):
    """Converts a string to a title string."""
    # verify the input
    if not isinstance(value, str):
        raise TypeError("The value must be a string.")
    return value.title()

@register.filter
def bold_shall(value):
    """Bold the word 'shall' in a string."""
    # verify the input
    if not isinstance(value, str):
        raise TypeError("The value must be a string.")
    return mark_safe(strip_tags(value).replace("shall", "<b>shall</b>"))