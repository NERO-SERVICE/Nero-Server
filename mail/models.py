from django.db import models
from django.conf import settings

class Mail(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    suggestion = models.TextField()

    def __str__(self):
        return f"Mail from {self.owner.username} at {self.created_at}"
