from django.db import models
from django.utils import timezone
from accounts.models import User
from PIL import Image, ImageOps
from django.contrib.postgres.indexes import GinIndex
import os
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, through='LikedPost')

    class Meta:
        verbose_name = "게시물"
        verbose_name_plural = "게시물"
        indexes = [
            GinIndex(fields=['content'], name='content_gin_index', opclasses=['gin_trgm_ops']),
        ]


    def __str__(self):
        return f"Post {self.post_id} by {self.user.nickname}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img = ImageOps.exif_transpose(img)  # 이미지 회전 정보 처리
        
        # 짧은 쪽을 기준으로 정사각형으로 중앙 크롭
        width, height = img.size
        if width > height:
            # 가로가 더 길 경우, 중앙에서 양쪽을 잘라 세로에 맞추어 정사각형으로 만듦
            left = (width - height) / 2
            top = 0
            right = (width + height) / 2
            bottom = height
        else:
            # 세로가 더 길 경우, 중앙에서 위아래를 잘라 가로에 맞추어 정사각형으로 만듦
            left = 0
            top = (height - width) / 2
            right = width
            bottom = (height + width) / 2
        img = img.crop((left, top, right, bottom))

        # 크롭한 이미지를 800x800으로 리사이징
        target_size = (800, 800)
        img = img.resize(target_size, Image.LANCZOS)

        # 초기 압축 품질 설정
        quality = 90
        img_format = 'JPEG'
        
        # 이미지 용량이 1MB 이하가 될 때까지 품질을 조정하며 저장
        while True:
            img.save(self.image.path, format=img_format, quality=quality)
            if os.path.getsize(self.image.path) <= 1 * 1024 * 1024:  # 1MB 이하인지 확인
                break
            quality -= 5  # 품질을 5씩 낮춤
            if quality < 10:  # 최소 품질 제한
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


class Report(models.Model):
    REPORT_CHOICES = [
        ('post_report', '게시물 신고'),
        ('post_block', '게시물 차단'),
        ('author_report', '작성자 신고'),
    ]
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "게시물 신고"
        verbose_name_plural = "게시물 신고"

    def __str__(self):
        return f"{self.report_type} by {self.reporter.nickname} on Post {self.post.post_id if self.post else 'N/A'}"
    

class CommentReport(models.Model):
    REPORT_CHOICES = [
        ('comment_report', '댓글 신고'),
        ('comment_block', '댓글 차단'),
        ('author_report', '작성자 신고'),
    ]
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reports')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "댓글 신고"
        verbose_name_plural = "댓글 신고"

    def __str__(self):
        return f"{self.report_type} by {self.reporter.nickname} on Comment {self.comment.comment_id if self.comment else 'N/A'}"


class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_post_relations')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_by_users')
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Liked Post'
        verbose_name_plural = 'Liked Posts'

    def __str__(self):
        return f"{self.user.nickname} liked Post {self.post.post_id}"