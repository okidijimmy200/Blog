from django import template
from ..models import POST
from django.db.models import Count
# import mark safe & markdown
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
'''template tags module needs to contain
a variable called register to be a valid tag library'''
'''to register by different name @register.simple_tag(name='my_tag').'''
@register.simple_tag 
def total_posts():
    return POST.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''template tag will accept an optional count parameter that defaults to
5. wch allows us specify the number of posts we want to display.'''
    latest_posts = POST.published.order_by('-publish')[:count]
    # template that has to be rendered
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    '''annotate() function to aggregate the total number of comments for
each post. Count aggregation function to store the number of comments in the computed field total_comments for each Post object'''
    return POST.published.annotate(
        total_comments=Count('comments') 
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
