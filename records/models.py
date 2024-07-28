from django.db import models

SERVEY_TYPE_CHOICES=(
    ('하루설문','하루설문'),
    ('부작용','부작용'),
    ('셀프기록','셀프기록'),
)

SYMPTOM_MAIN_TYPE_CHOICES=(
    ('소화기계','소화기계'),
    ('정신/심리','정신/심리'),
    ('신경계','신경계'),
    ('심혈관계','심혈관계'),
    ('생식기계','생식기계'),
    ('직접입력','직접입력'),
)

class QuestionList(models.Model):
    questionId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=SERVEY_TYPE_CHOICES)
    content = models.TextField()

    def __str__(self):
        return self.content

class ServeyLog(models.Model):
    logId = models.AutoField(primary_key=True)
    questions = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
    today = models.DateTimeField(auto_now_add=True)
    answer = models.TextField()
    

class SymptomCare(models.Model):
    symptomId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=SYMPTOM_MAIN_TYPE_CHOICES)
    content = models.CharField(max_length=10)

    def __str__(self):
        return self.content

class SymptomLog(models.Model):
    symptomLogId = models.AutoField(primary_key=True)
    symptomQuestions = models.ForeignKey(SymptomCare, on_delete=models.CASCADE)
    today = models.DateTimeField(auto_now_add=True)
    answer = models.TextField()