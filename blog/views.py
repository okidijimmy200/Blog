from django.shortcuts import render, get_object_or_404
from .models import POST, Comment
# use of pagination
from django.core.paginator import Paginator, EmptyPage,\
                                    PageNotAnInteger

# importing EmailPostform
from .forms import EmailPostForm, CommentForm

# importing core mail
from django.core.mail import send_mail

# import taggit
from taggit.models import Tag
# adding the retrieve post by similarity
from django.db.models import Count

 


# use of class based views
from django.views.generic import ListView

def post_list(request, tag_slug=None):
    # '''retrieving all the posts with the published status using the published manager'''
    object_list = POST.published.all()
    # adding the tag functionality
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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
                'posts': posts,
                'tag':tag})


'''view to display a single post'''
def post_detail(request, year, month, day, post):
    ''' get_object_or_404 retrieves the object that matches the given parameters or
launches an HTTP 404 '''
    post = get_object_or_404(POST, slug=post,
                            status='published', publish__year=year,
                            publish__month=month,publish__day=day)
    
    # list of all active comments for this post
    '''We use the manager for related objects we defined as comments using the
related_name attribute of the relationship in the Comment model.'''
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            '''We create a new Comment object by calling the form's save()
method and assign it to the new_comment variable'''
            # create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()

    # to perform aggregation count(list of similar posts)
    '''We retrieve a Python	list	of	IDs	for	the	tags	of	the	current post.	The	values_list() QuerySet	returns	tuples	with	the values	for	the	given	fields.	We	pass	flat=True	to	it	to	get	a	flat list	like	[1,	2,	3,	...].'''
    post_tags_ids = post.tags.values_list('id', flat=True)
    '''We	get	all	posts	that	contain	any	of	these	tags,excluding the current	post itself'''
    similar_posts = POST.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    '''	We	use	the	Count	aggregation	function	to	generate	a calculated	field—same_tags—that	contains	the	number	of	tags
shared	with	all	the	tags	queried. '''
    '''We	order	the	result	by	the	number	of	shared	tags (descending	order)	and	by	publish	to	display	recent	posts	first for	the	posts	with	the	same	number	of	shared	tags.	We	slice the	result	to	retrieve	only	the	first	four	posts.'''
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags', '-publish')[:4]

    return render(request,
                        'blog/post/detail.html',
                        {'post': post,
                        'comments': comments,
                        'new_comment': new_comment,
                        'comment_form': comment_form,
                        'similar_posts': similar_posts})

# use of classbased views
class PostListView(ListView):
    # Use QuerySet instead of retrieving all objects
    queryset = POST.published.all()
    # context variable posts for the query results.
    context_object_name = 'posts'
    # Paginate the result displaying three objects per page.
    paginate_by = 3
    template_name = 'blog/post/list.html'


# this view takes the request object and the post_id variable as parameters.
def post_share(request, post_id):
    # retrieve post by id
    '''get_object_or_404() shortcut to retrieve the post by ID and make sure that the retrieved post has a published
status.'''
    post = get_object_or_404(POST, id=post_id, status='published')
    # variable set to true only when the post was sent
            # later we will use sent in template to display a success message when the form is successfully submitted
    sent = False

# We differentiate whether the form was submitted or not based on the request method 
# and submit the form using POST.
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        # we validate the submitted data using the form's is_valid() method.
        
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # ...send data
            # we have to include a link to the post in the email, we use et_absolute_url()
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # We build the subject and the message body of the email
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            # when the post is sent,its set to true
            sent = True
    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form':form,
                                                    'sent': sent})

'''When the view is loaded initially with a GET request, we
create a new form instance that will be used to display the
empty form in the template:
form = EmailPostForm()
'''

'''The user fills in the form and submits it via POST'''