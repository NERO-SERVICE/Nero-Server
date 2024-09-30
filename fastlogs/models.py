from django.db import models
from django.conf import settings

class DailyLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.nickname} - {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = "빠른메모"
        verbose_name_plural = "빠른메모"
