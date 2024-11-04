from django.db import models
from django.utils import timezone
from accounts.models import SoftDeletableModel, User

class Post(SoftDeletableModel):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='post_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        verbose_name = "게시물"
        verbose_name_plural = "게시물"

    def __str__(self):
        return f"Post {self.post_id} by {self.user.nickname}"

class Comment(SoftDeletableModel):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글"

    def __str__(self):
        return f"Comment {self.comment_id} by {self.user.nickname} on Post {self.post.post_id}"
