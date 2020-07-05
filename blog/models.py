from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#the reverse() method allows you to build
# URLs by their name and passing optional parameters.
from django.urls import reverse
# import taggit
from taggit.managers import TaggableManager


# creating a custom manager
class PublishedManager(models.Manager):
    # this returns the queyset to be executed
    # override this method to include our custom filter in
    # the final QuerySet.
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                          .filter(status='published')

class POST(models.Model):

    # The __str__() method is the default human-readable representation
    # of the object used in administration site and others
    def __str__(self):
        return self.title

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # This is the field for the post title.
    title = models.CharField(max_length=250)
    # slug this field is used in our URLs to build friendly URLs for our  users
    #unique_for_date is used to build URLs for post using slug and dat of publish
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    """We are telling Django that each post is written by a user, and a user can write any number of posts
    The on_delete parameter specifies the behavior to adopt when the referenced object is deleted
    the related_name attribute shows us the reverse relationship from user to post to enable us get related objects easily"""
    author = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='blog_post')
    # body of the post.
    body = models.TextField()
    # publish --This datetime indicates when the post was published.
    publish = models.DateTimeField(default=timezone.now)
    # created--when the post ws created, we use auto_now_add so the date is auto-matically saved when creating object
    created = models.DateTimeField(auto_now_add=True)
    """updated--this shows when the post ws last updated, using auto_now here, the date will be
    updated automatically when saving an object."""
    updated = models.DateTimeField(auto_now=True)
    # status--shows status of a post, we use choices parameter
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')
    # meta is used to sort results in publish field in descending order by default
    # decending order, we use -ve prefix
    # so posts published recently will appear first
    class Meta:
        ordering = ('-publish',)


    # default manager
    objects = models.Manager()
#     our custom manager
    published = PublishedManager()
    # including the tag manager
    tags = TaggableManager()

    '''The convention in Django is to add a get_absolute_url() method to the
model that returns the canonical URL of the object.'''
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug])



# creating the comments section
class Comment(models.Model):
    # The related_name attribute allows us to name the attribute that we use for
# the relation
    post = models.ForeignKey(POST, on_delete=models.CASCADE,
                            related_name='comments')

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    '''created field to sort comments in a chronological order by default.'''
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    ''' active boolean field that we will use to
manually deactivate inappropriate comments'''
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


