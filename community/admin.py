from django.contrib import admin
from .models import Post, Comment, PostImage, Report, CommentReport

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

class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'report_type', 'reporter', 'post', 'get_reported_post_author', 
        'get_reported_post_content', 'description', 'created_at'
    )
    readonly_fields = ('reporter', 'created_at')

    def get_reported_post_author(self, obj):
        return obj.post.user.nickname if obj.post and obj.post.user else None
    get_reported_post_author.short_description = '신고된 게시물 작성자'

    def get_reported_post_content(self, obj):
        return obj.post.content if obj.post else None
    get_reported_post_content.short_description = '신고된 게시물 내용'

class CommentReportAdmin(admin.ModelAdmin):
    list_display = (
        'report_type', 'reporter', 'comment', 'get_reported_comment_author', 
        'get_reported_comment_content', 'description', 'created_at'
    )
    readonly_fields = ('reporter', 'created_at')

    def get_reported_comment_author(self, obj):
        return obj.comment.user.nickname if obj.comment and obj.comment.user else None
    get_reported_comment_author.short_description = '신고된 댓글 작성자'

    def get_reported_comment_content(self, obj):
        return obj.comment.content if obj.comment else None
    get_reported_comment_content.short_description = '신고된 댓글 내용'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostImage)
admin.site.register(Report, ReportAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
