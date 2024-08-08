from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    kakaoId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField(default=36.5) 
    email = models.EmailField(unique=True, null=True, blank=True, default='')

    def __str__(self):
        return self.kakaoId