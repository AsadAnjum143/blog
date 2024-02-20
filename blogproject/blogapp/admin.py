from django.contrib import admin
from .models import PostTable, CommentTable
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title','slug','author','body_blog','publish_blog','creation_blog','updation_blog','status')
    list_filter = ('status','author')
    search_fields = ('title','body_blog','author')
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status','publish_blog']
    
admin.site.register(PostTable, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','body','created','updated','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')
    
admin.site.register(CommentTable, CommentAdmin)