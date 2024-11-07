from django.db import models
from django.utils import timezone
from accounts.models import User
from PIL import Image, ImageOps
import os

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

        img = Image.open(self.image.path)
        img = ImageOps.exif_transpose(img)
        max_size = (600, 600)
        img = img.resize(max_size, Image.LANCZOS)  # LANCZOS 필터로 고품질 리사이징

        # 초기 압축 품질 설정
        quality = 90
        img_format = 'JPEG'
        
        # 이미지가 1MB 이하가 될 때까지 품질을 조정하면서 저장
        while True:
            img.save(self.image.path, format=img_format, quality=quality)
            if os.path.getsize(self.image.path) <= 1 * 1024 * 1024:  # 1MB 이하인지 확인
                break
            quality -= 5  # 품질을 5씩 낮춤
            if quality < 10:  # 최소 품질 제한 (10 이하로 떨어지지 않도록)
                break

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
