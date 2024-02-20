from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'published')
    

class PostTable(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published')) # Incase if we want to keep in draft and alter later
    
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'blog_posts') #ManyToOne Relationship, One author might be posting many blogs
    body_blog = models.TextField() # for posting huge content
    publish_blog = models.DateField(default = timezone.now) # Date of blog post
    creation_blog = models.DateField(auto_now_add = True) # Date of creationg of blog
    updation_blog = models.DateField(auto_now = True) # Date of updation of blog
    slug = models.SlugField(max_length = 50, unique_for_date = 'publish_blog') #Giving the endpoint in url and to avoid the clashes with two same title name
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, default = 'draft')
    
    objects = CustomManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-publish_blog',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail',args = [self.publish_blog.year, self.publish_blog.strftime('%m'),self.publish_blog.strftime('%d'),self.slug])
                    #calling the function name and passing this arguments
    
class CommentTable(models.Model):
    post = models.ForeignKey(PostTable, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default = True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return 'Commented by {} on {}'.format(self.name,self.post)