from django.db import models

class Today(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    next_appointment_date = models.DateField()

    def __str__(self):
        return f"Today Entry - {self.created_at}"


class Survey(models.Model):
    TODAY_SURVEY_ANSWERS = [
        ('1', '매우 나쁨'),
        ('2', '나쁨'),
        ('3', '보통'),
        ('4', '좋음'),
        ('5', '매우 좋음'),
    ]
    
    today = models.OneToOneField(Today, on_delete=models.CASCADE, related_name='survey')
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=1, choices=TODAY_SURVEY_ANSWERS)

    def __str__(self):
        return f"Survey - {self.question} : {self.answer}"


class SideEffect(models.Model):
    SIDE_EFFECT_ANSWERS = [
        ('1', '전혀 없음'),
        ('2', '거의 없음'),
        ('3', '조금 있음'),
        ('4', '꽤 있음'),
        ('5', '많이 있음'),
    ]
    
    today = models.OneToOneField(Today, on_delete=models.CASCADE, related_name='side_effect')
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=1, choices=SIDE_EFFECT_ANSWERS)

    def __str__(self):
        return f"Side Effect - {self.question} : {self.answer}"


class SelfRecord(models.Model):
    today = models.OneToOneField(Today, on_delete=models.CASCADE, related_name='self_record')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Self Record - {self.created_at}"
