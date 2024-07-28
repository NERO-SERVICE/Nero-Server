from django.db import models
from today.models import Today

class QuestionList(models.Model):
    questionId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.content

class ServeyLog(models.Model):
    logId = models.AutoField(primary_key=True)
    questions = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
    today = models.ForeignKey(Today, on_delete=models.CASCADE)
    answer = models.TextField()
    

class SymptomCare(models.Model):
    symptomId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.content

class SymptomLog(models.Model):
    symptomLogId = models.AutoField(primary_key=True)
    symptomQuestions = models.ForeignKey(SymptomCare, on_delete=models.CASCADE)
    today = models.ForeignKey(Today, on_delete=models.CASCADE)
    answer = models.TextField()