from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import POST


class LatestPostFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog'

    '''The items() method retrieves the objects to be included in the feed.'''
    def items(self):
        return POST.published.all()[:5]

    '''The item_title() and item_description() methods receive each object returned
by items() and return the title and description for each item.'''
    def item_title(self,item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)