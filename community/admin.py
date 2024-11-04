from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('content', 'user__nickname')
    list_filter = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'post', 'user', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('content', 'user__nickname', 'post__content')
    list_filter = ('created_at', 'updated_at')