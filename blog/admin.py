from django.contrib import admin
from .models import POST, Comment

# this shows how we can display attributes in our admin
@admin.register(POST)
class POSTAdmin(admin.ModelAdmin):
    # fields displayed on the post list page are the ones you specified in the list_display attribute.
    list_display = ('title', 'slug', 'author', 'publish'
                    , 'status')
#   The list page now includes a right sidebar that allows you to filter the results by the
    # fields included in the list_filter attribute
    list_filter = ('status', 'created', 'publish', 'author')
    '''A Search bar has appeared on the page because we have defined a list of searchable
        fields using the search_fields attribute.'''
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    # the author field is displayed with a lookup widget that can scale much better than a drop-down select
    # input when you have thousands of users,
    raw_id_fields = ('author',)
    # Just below the Search bar,
    # there are navigation links to navigate through a date hierarchy:by the date_hierarchy attribute
    date_hierarchy = 'publish'
    # the posts are ordered by Status and Publish columns by default bse we have specified the default order using the ordering attribute.
    ordering = ('status', 'publish')

'''Now, click on the Add Post link As you type the title of a new post, 
the slug field is filled in automatically'''

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')





# Register your models here.
