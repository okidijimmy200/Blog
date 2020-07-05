from django import template
from ..models import POST

register = template.library()

@register.simple_tag
def total_posts():
    return POST.published.count()