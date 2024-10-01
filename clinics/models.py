from django.db import models
from django.conf import settings

# DrugArchive 모델: 서버에 저장된 약물 아카이브
class DrugArchive(models.Model):
    archiveId = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=100)
    target = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.drugName
    
    class Meta:
        verbose_name = "서버 저장 약물 아카이브"
        verbose_name_plural = "서버 저장 약물 아카이브"


# MyDrugArchive 모델: 개별 사용자가 선택한 약물
class MyDrugArchive(models.Model):
    myArchiveId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archive = models.ForeignKey(DrugArchive, on_delete=models.CASCADE, related_name='my_drug_archives')

    def __str__(self):
        return f"{self.owner}'s selected {self.archive.drugName}"
    
    class Meta:
        verbose_name = "처방 개별 약"
        verbose_name_plural = "처방 개별 약"


# Clinics 모델: 진료 기록
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
        verbose_name = "진료기록"
        verbose_name_plural = "진료기록"


# Drug 모델: 진료 기록에 연결된 약물 정보
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
        
    class Meta:
        verbose_name = "처방약물"
        verbose_name_plural = "처방약물"
