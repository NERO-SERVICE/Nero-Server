from django.db import models
from django.conf import settings

class QuestionType(models.Model):
    type_code = models.CharField(max_length=20, unique=True)
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name


class QuestionSubtype(models.Model):
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='subtypes')
    subtype_code = models.CharField(max_length=20)
    subtype_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('type', 'subtype_code')

    def __str__(self):
        return self.subtype_name


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='questions')
    question_subtype = models.ForeignKey(QuestionSubtype, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "질문모음"
        verbose_name_plural = "질문모음"


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Today(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    next_appointment_date = models.DateField(null=True)

    def __str__(self):
        return f"Today Entry - {self.owner.nickname} - {self.created_at}"


class AnswerChoice(models.Model):
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='answer_choices')
    question_subtype = models.ForeignKey(QuestionSubtype, on_delete=models.CASCADE, related_name='answer_choices')
    answer_code = models.CharField(max_length=1)
    answer_text = models.CharField(max_length=255)

    def __str__(self):
        return self.answer_text

    class Meta:
        unique_together = ('question_type', 'question_subtype', 'answer_code')


class Response(AbstractBaseModel):
    RESPONSE_TYPE_CHOICES = [
        ('survey', 'Survey'),
        ('side_effect', 'Side Effect'),
    ]
    
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE, null=True)
    response_type = models.CharField(max_length=20, choices=RESPONSE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.get_response_type_display()} Response - {self.question.question_text} - {self.answer}"


class SurveySession(models.Model):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='survey_sessions')
    response_type = models.CharField(max_length=20, choices=Response.RESPONSE_TYPE_CHOICES)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.response_type} session on {self.today.created_at.date()}"


class SelfRecord(AbstractBaseModel):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='self_records')
    content = models.TextField()

    def __str__(self):
        return f"Self Record - {self.created_at}"
    
    class Meta:
        verbose_name = "셀프기록"
        verbose_name_plural = "셀프기록"


class SurveyCompletion(models.Model):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='survey_completions')
    response_type = models.CharField(max_length=20, choices=Response.RESPONSE_TYPE_CHOICES)
    question_subtype = models.ForeignKey(QuestionSubtype, on_delete=models.CASCADE, related_name='survey_completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('today', 'response_type', 'question_subtype')

    def __str__(self):
        return f"{self.response_type} completed for {self.question_subtype} on {self.today}"
