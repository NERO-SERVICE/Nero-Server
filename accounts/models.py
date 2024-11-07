from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image, ImageOps

class SoftDeleteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeletableModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class User(AbstractUser, SoftDeletableModel):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    kakaoId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    appleId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True, default='')
    createdAt = models.DateTimeField(default=timezone.now)
    birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    is_product_writer = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    objects = SoftDeleteManager()  # SoftDeleteManager를 기본 매니저로 사용
    all_objects = models.Manager()  # 모든 객체를 관리하는 기본 매니저

    class Meta:
        verbose_name = "유저관리"
        verbose_name_plural = "유저관리"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            img = Image.open(self.profile_image.path)
            img = ImageOps.exif_transpose(img)  # EXIF 데이터 기반 회전 처리
            max_size = (300, 300)
            img.thumbnail(max_size, Image.LANCZOS)
            img.save(self.profile_image.path)

class Memories(SoftDeletableModel):
    memoryId = models.AutoField(primary_key=True)
    userId = models.OneToOneField(User, on_delete=models.CASCADE, related_name='memories')
    items = JSONField(blank=True, default=list)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "챙길거리"
        verbose_name_plural = "챙길거리"
