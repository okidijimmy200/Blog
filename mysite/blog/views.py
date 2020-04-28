from django.shortcuts import render, get_object_or_404
from .models import POST


def post_list(request):
    '''retrieving all the posts with the published status using the published manager'''
    posts = POST.published.all()
    return render(request,
    'blog/post/list.html',
    {'posts': posts})


'''view to display a single post'''
def post_detail(request, year, month, day, post):
    ''' get_object_or_404 retrieves the object that matches the given parameters or
launches an HTTP 404 '''
    post = get_object_or_404(POST, slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day)
    return render(request,
    'blog/post/detail.html',
    {'post': post})