from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import JSONField

class User(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    kakaoId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True, default='')
    createdAt = models.DateTimeField(default=timezone.now)
    birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    

class Memories(models.Model):
    memoryId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    items = JSONField(blank=True, default=list)