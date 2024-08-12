from django.db import models
from django.conf import settings

# Create your models here.
class DrfClinics(models.Model):
    clinicId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recentDay = models.DateTimeField(auto_now_add=True)
    nextDay = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
class DrfDrug(models.Model):
    drugId = models.AutoField(primary_key=True)
    item = models.ForeignKey(DrfClinics, related_name='drugs', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[
        ('a', '콘서타 18mg'),
        ('b', '콘서타 27mg'),
        ('c', '콘서타 36mg'),
        ('d', '메디카넷 18mg'),
        ('e', '페로스핀 18mg'),
    ])
    number = models.IntegerField(default=0)
    time = models.CharField(max_length=50, choices=[
        ('morning', '아침'),
        ('lunch', '점심'),
        ('evening', '저녁'),
    ])

    def __str__(self):
        return f"Drug {self.drugId} for {self.item.title}"