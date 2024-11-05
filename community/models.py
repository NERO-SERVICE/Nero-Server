from django.db import models
from django.utils import timezone
from accounts.models import User
from PIL import Image

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        verbose_name = "게시물"
        verbose_name_plural = "게시물"

    def __str__(self):
        return f"Post {self.post_id} by {self.user.nickname}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 리사이징을 위한 이미지 열기
        img = Image.open(self.image.path)

        # 리사이징 조건 설정 (최대 가로, 세로 크기 800px)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.ANTIALIAS)
        img.save(self.image.path)  # 리사이징된 이미지를 덮어쓰기

    def __str__(self):
        return f"Image for Post {self.post.post_id}"


class Comment(models.Model):
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
