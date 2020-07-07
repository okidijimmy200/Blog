from django.contrib.sitemaps import Sitemap
from .models import POST


'''We create a custom sitemap by inheriting the Sitemap class of the
sitemaps module'''
class PostSitemap(Sitemap):
    '''The changefreq and priority attributes indicate the
change frequency of your post pages and their relevance in your
website max value is 1'''
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return POST.published.all()
    '''The lastmod method receives each object returned
by items() and returns the last time the object was modified'''
    def lastmod(self, obj):
        return obj.updated