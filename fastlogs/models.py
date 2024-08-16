from django.db import models
from django.conf import settings

class DailyLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"{self.owner.nickname} - {self.date}"

    class Meta:
        unique_together = ('owner', 'date')
        ordering = ['-date']
