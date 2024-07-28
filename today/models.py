from django.db import models
from accounts.models import User

class Today(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todays')
    date = models.DateField()

    def __str__(self):
        return f"{self.userId.username} - {self.date}"