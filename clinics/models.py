from django.db import models
from django.conf import settings

class DrfDrugArchive(models.Model):
    drugName = models.CharField(max_length=100)
    target = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.drugName

class DrfClinics(models.Model):
    clinicId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recentDay = models.DateTimeField()
    nextDay = models.DateTimeField()
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    clinicLatitude = models.FloatField(null=True, blank=True)
    clinicLongitude = models.FloatField(null=True, blank=True)
    locationLabel = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updatedAt']

class DrfDrug(models.Model):
    drugId = models.AutoField(primary_key=True)
    item = models.ForeignKey(DrfClinics, related_name='drugs', on_delete=models.CASCADE)
    drugArchive = models.ManyToManyField(DrfDrugArchive)
    number = models.IntegerField(default=0)
    initialNumber = models.IntegerField(default=0)
    time = models.CharField(max_length=50, choices=[
        ('아침', '아침'),
        ('점심', '점심'),
        ('저녁', '저녁'),
    ])
    allow = models.BooleanField(default=True)

    def __str__(self):
        return f"Drugs for {self.item.title}"
    
    def consume_one(self):
        if self.number > 0:
            self.number -= 1
            self.save()
        else:
            raise ValueError("No more drugs left to consume.")
    
    def reset_allow(self):
        self.allow = True
        self.save()
