from django.db import models
from django.conf import settings

class YearlyDoseLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    doseAction = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username} - {self.date} - Dose: {self.doseAction}"
    
    class Meta:
        verbose_name = "연간관리 - 약복용"
        verbose_name_plural = "연간관리 - 약복용"


class YearlySideEffectLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    sideEffectAction = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username} - {self.date} - Side Effect: {self.sideEffectAction}"
    
    class Meta:
        verbose_name = "연간관리 - 부작용"
        verbose_name_plural = "연간관리 - 부작용"
