from blogapp.models import PostTable
from django import template
from django.db.models import Count
register = template.Library()

@register.simple_tag(name = 'my_tag')
def total_posts():
    return PostTable.objects.count()

@register.inclusion_tag('blogapp/latest_posts.html')
def show_latest_posts():
    latest_posts = PostTable.objects.order_by('-publish_blog')[:2]
    return {'latest_posts':latest_posts}

@register.simple_tag()
def get_most_commented_posts(total = 3):
    return PostTable.objects.annotate(total_comments = Count('comments')).order_by('-total_comments')[:total] # getting the comments and ordering