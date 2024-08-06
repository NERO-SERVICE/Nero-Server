from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)