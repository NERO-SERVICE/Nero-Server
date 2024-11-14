from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    CommentCreateView,
    CommentListView,
    CommentDetailView,
    LikePostView,
    LikeCommentView,
    ReportCreateView,
    CommentReportCreateView,
    LikedPostListView,
    MyPostsListView,
    PopularPostListView,
)

app_name = 'community'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('comments/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment'),
    path('reports/create/', ReportCreateView.as_view(), name='report_create'),
    path('comments/reports/create/', CommentReportCreateView.as_view(), name='comment_report_create'),
    path('posts/liked/', LikedPostListView.as_view(), name='liked_post_list'),
    path('posts/mine/', MyPostsListView.as_view(), name='my_post_list'),
    path('posts/popular/', PopularPostListView.as_view(), name='popular_post_list'),
]