from django.db import models
from django.conf import settings

class DrugArchive(models.Model):
    archiveId = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=100)
    target = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.drugName


class MyDrugArchive(models.Model):
    myArchiveId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archiveId = models.IntegerField()
    drugName = models.CharField(max_length=100)
    target = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.owner}'s selected {self.drugName}"


class Clinics(models.Model):
    clinicId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recentDay = models.DateTimeField()
    nextDay = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.recentDay.strftime('%Y-%m-%d')

    class Meta:
        ordering = ['-updatedAt']


class Drug(models.Model):
    drugId = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinics, related_name='drugs', on_delete=models.CASCADE)
    myDrugArchive = models.ForeignKey(MyDrugArchive, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    initialNumber = models.IntegerField(default=0)
    time = models.CharField(max_length=50, choices=[
        ('아침', '아침'),
        ('점심', '점심'),
        ('저녁', '저녁'),
    ])
    allow = models.BooleanField(default=True)

    def __str__(self):
        return f"Drugs for {self.clinic.recentDay.strftime('%Y-%m-%d')}"

    def consume_one(self):
        if self.number > 0:
            self.number -= 1
            self.save()
        else:
            raise ValueError("No more drugs left to consume.")

    def reset_allow(self):
        self.allow = True
        self.save()