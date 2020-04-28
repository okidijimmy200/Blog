from django.shortcuts import render, get_object_or_404
from .models import POST

from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

def post_list(request):
    # '''retrieving all the posts with the published status using the published manager'''
    object_list = POST.published.all()
    '''We instantiate the Paginator class with the number of objects to display on each page'''
    paginator = Paginator(object_list, 3) # 3 posts in each page
    '''page GET parameter that indicates the current page we are on'''
    page = request.GET.get('page')
  
    try:
          # objects for the desired page calling the page() method of Paginator.
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                'blog/post/list.html',
                {'page': page,
                'posts': posts})


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