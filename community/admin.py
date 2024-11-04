
from django.contrib import admin
from .models import Post, Comment, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id_display', 'user', 'content', 'created_at', 'updated_at', 'get_likes_count', 'get_comments_count')
    inlines = [PostImageInline]
    readonly_fields = ('get_likes_count', 'get_comments_count')

    def post_id_display(self, obj):
        return obj.post_id
    post_id_display.short_description = 'Post ID'

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes Count'

    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Comments Count'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostImage)