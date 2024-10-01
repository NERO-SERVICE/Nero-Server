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
    question_subtype = models.ForeignKey(QuestionSubtype, on_delete=models.CASCADE, related_name='answer_choices')
    answer_code = models.CharField(max_length=1)
    answer_text = models.CharField(max_length=255)

    def __str__(self):
        return self.answer_text

    class Meta:
        unique_together = ('question_subtype', 'answer_code')


class SurveyResponse(AbstractBaseModel):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='survey_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='survey_responses')
    answer = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Survey Response - {self.question.question_text} - {self.answer}"


class SideEffectResponse(AbstractBaseModel):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='side_effect_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='side_effect_responses')
    answer = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Side Effect Response - {self.question.question_text} - {self.answer}"


class SelfRecord(AbstractBaseModel):
    today = models.ForeignKey(Today, on_delete=models.CASCADE, related_name='self_records')
    content = models.TextField()

    def __str__(self):
        return f"Self Record - {self.created_at}"
    
    class Meta:
        verbose_name = "셀프기록"
        verbose_name_plural = "셀프기록"
