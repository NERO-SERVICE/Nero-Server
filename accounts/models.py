from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kakao_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
