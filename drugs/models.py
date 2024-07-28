from django.db import models
from accounts.models import User

class DrugList(models.Model):
    id = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    
class ClinicLog(models.Model):
    clinicId = models.AutoField(primary_key=True)
    drug = models.ForeignKey(DrugList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    clinicDate = models.DateTimeField()
    nextDate = models.DateTimeField()
    doseTime = models.CharField(max_length=100)
    clinicNote = models.TextField()