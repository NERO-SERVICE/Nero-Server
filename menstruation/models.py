from django.db import models
from django.conf import settings

class Menstruation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    notes = models.TextField(blank=True, null=True)

    @property
    def cycleLength(self):
        if self.startDate and self.endDate:
            return (self.endDate - self.startDate).days
        return None

    def __str__(self):
        return f"{self.owner.username}의 생리 주기 ({self.startDate} - {self.endDate})"
    
    class Meta:
        verbose_name = "생리주기"
        verbose_name_plural = "생리주기"
        ordering = ['-startDate']  # 최근 날짜의 생리주기가 위에 오도록
        indexes = [
            models.Index(fields=['owner', 'startDate']),
        ]
