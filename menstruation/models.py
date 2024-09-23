from django.db import models
from django.conf import settings

class Menstruation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    cycleLength = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.startDate and self.endDate:
            self.cycleLength = (self.endDate - self.startDate).days
        super(Menstruation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner.username}의 생리 주기 ({self.startDate} - {self.endDate})"
