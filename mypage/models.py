from django.db import models
from django.conf import settings

class YearlyDoseLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    doseAction = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username} - {self.date}: {'Dose' if self.doseAction else 'No Dose'}"

    class Meta:
        unique_together = ('owner', 'date')
        ordering = ['date']


class YearlySideEffectLog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    sideEffectAction = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username} - {self.date}: {'Side Effect' if self.sideEffectAction else 'No Side Effect'}"

    class Meta:
        unique_together = ('owner', 'date')
        ordering = ['date']
