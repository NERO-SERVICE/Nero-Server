from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class SoftDeleteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    kakaoId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True, default='')
    createdAt = models.DateTimeField(default=timezone.now)
    birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    is_product_writer = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()  # SoftDeleteManager를 기본 매니저로 사용
    all_objects = models.Manager()  # 모든 객체를 관리하는 기본 매니저

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class Memories(models.Model):
    memoryId = models.AutoField(primary_key=True)
    userId = models.OneToOneField(User, on_delete=models.CASCADE, related_name='memories')
    items = JSONField(blank=True, default=list)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()  # SoftDeleteManager를 기본 매니저로 사용
    all_objects = models.Manager()  # 모든 객체를 관리하는 기본 매니저

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()