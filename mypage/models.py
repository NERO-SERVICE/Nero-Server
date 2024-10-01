from django.db import models
from django.conf import settings

class YearlyLog(models.Model):
    LOG_TYPES = [
        ('dose', '약복용'),
        ('side_effect', '부작용'),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    action = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username} - {self.date} - {self.log_type.capitalize()}: {self.action}"
    
    class Meta:
        verbose_name = "연간관리 기록"
        verbose_name_plural = "연간관리 기록"
        unique_together = ('owner', 'date', 'log_type')
        indexes = [
            models.Index(fields=['owner', 'date', 'log_type']),
        ]
