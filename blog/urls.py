from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'


urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # use of class based views
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    views.post_detail,
    name='post_detail'),
    # url for post_share
    path('<int:post_id>/share/', 
        views.post_share, name='post_share'),
    # listing posts by tag
    # calling the view using the tag_slug	parameter
    # We use a	slug path converter	for	matching the	parameter	as	a	lowercase	string	with ASCII	letters	or	numbers,	plus	the	hyphen	and	underscore characters.
    path('tag/<slug:tag_slug>/', views.post_list,	name='post_list_by_tag'),
    # url for feeds
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]