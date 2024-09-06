from django.db import models
from django.conf import settings

class Question(models.Model):
    QUESTION_TYPES = [
        ('survey', 'Survey'),
        ('side_effect', 'Side Effect'),
    ]
    
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
        return self.question_text


class Today(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    next_appointment_date = models.DateField(null=True)

    def __str__(self):
        return f"Today Entry - {self.owner.nickname} - {self.created_at}"


class SurveyResponse(models.Model):
    TODAY_SURVEY_ANSWERS = [
        ('1', '매우 나쁨'),
        ('2', '나쁨'),
        ('3', '보통'),
        ('4', '좋음'),
        ('5', '매우 좋음'),
    ]

    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='survey_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='survey_responses')
    answer = models.CharField(max_length=1, choices=TODAY_SURVEY_ANSWERS, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.created_at.strftime('%Y-%m-%d %H:%M')
        return f"Today Entry - {self.owner.nickname} - {formatted_date}"


class SideEffectResponse(models.Model):
    SIDE_EFFECT_ANSWERS = [
        ('1', '전혀 없음'),
        ('2', '거의 없음'),
        ('3', '조금 있음'),
        ('4', '꽤 있음'),
        ('5', '많이 있음'),
    ]

    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='side_effect_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='side_effect_responses')
    answer = models.CharField(max_length=1, choices=SIDE_EFFECT_ANSWERS, null=True)

    def __str__(self):
        return f"Side Effect Response - {self.question.question_text} : {self.answer}"


class SelfRecord(models.Model):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='self_records')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Self Record - {self.created_at}"
