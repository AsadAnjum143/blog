from django.shortcuts import render
from .models import PostTable
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailSendForm
from django.core.mail import send_mail
from .forms import CommentForm
from taggit.models import Tag

def post_list_view(request,tag_slug = None):
    data = PostTable.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        data = data.filter(tags__in = [tag])
    
    paginator = Paginator(object_list= data,per_page= 2)
    page_number = request.GET.get('page') # --> by default having the page
    
    try:
        data = paginator.page(page_number)
    
    except PageNotAnInteger:
        data = paginator.page(1)
        
    except EmptyPage:
        data = Paginator.page(paginator.num_pages)
    
    my_dict = {'posttable_list':data, 'tag':tag}
    return render(request=request, template_name="blogapp/posttable_list.html", context= my_dict)

#Class based View
class PostListView(ListView):
    model = PostTable
    paginate_by = 2

def post_detail_view(request,year,month, day, post):
    post = get_object_or_404(PostTable, slug = post,status = 'published', publish_blog__year = year, publish_blog__month = month, publish_blog__day = day)
    comments = post.comments.filter(active = True) #--> Collecting the comment
    csubmit = False
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False) #--> if any alteration has to be done so we are doing this orelse will save directly
            new_comment.post = post #--> fetching comment from post already posted
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    my_dict = {'post':post, 'form':form, 'csubmit':csubmit,'comments':comments}
    return render(request=request, template_name="blogapp/post_detail.html", context = my_dict)

def mail_send_view(request,id):
    post = get_object_or_404(PostTable,id = id, status = 'published')
    sent = False
    if request.method == "POST":
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #send_mail(subject="",message="",from_email="",recipient_list=[""]) --> Syntax
            subject = '{} ({})'.format(cd['name'],cd['email'],post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read the post at :\n {} \n\n {}\'s Comments: \n{}'.format(post_url, cd['name'], cd['comments'])
            send_mail(subject,message,'asadanjum54321@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailSendForm()
     
    my_dict = {'form':form, 'post':post, 'sent':sent}
    return render(request=request, template_name= 'blogapp/sharebymail.html', context= my_dict)
