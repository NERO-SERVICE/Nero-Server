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
]