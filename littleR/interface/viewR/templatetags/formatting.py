from django import template

register = template.Library()

@register.filter
def title_string(value):
    """Converts a string to a title string."""
    # verify the input
    if not isinstance(value, str):
        raise TypeError("The value must be a string.")
    return value.title()