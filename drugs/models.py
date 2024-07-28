from django.db import models
from accounts.models import User

TYPE_CHOICES=(
    ('아침','아침'),
    ('점심','점심'),
    ('저녁','저녁'),
)

DOSE_CHOICES=(
    ('mg','mg'),
    ('정','정'),
)

class DrugList(models.Model):
    id = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=DOSE_CHOICES)
    
    def __str__(self):
        return f"{self.drugName} {self.capacity}{self.unit}"
    
class ClinicLog(models.Model):
    clinicId = models.AutoField(primary_key=True)
    drug = models.ForeignKey(DrugList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    clinicDate = models.DateField()
    nextDate = models.DateField()
    doseTime = models.CharField(max_length=10, choices=TYPE_CHOICES)
    clinicNote = models.TextField()