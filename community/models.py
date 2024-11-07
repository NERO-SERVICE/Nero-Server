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

        # 이미지 리사이징 및 압축
        img = Image.open(self.image.path)
        max_size = (600, 600)
        img.thumbnail(max_size, Image.ANTIALIAS)

        # 압축 품질을 85로 설정하여 이미지 저장
        img.save(self.image.path, format='JPEG', quality=85)

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
