from django.contrib import admin
from .models import Today, SelfRecord, Question, QuestionType, QuestionSubtype, AnswerChoice, Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer', 'response_type']
    search_fields = ['today__created_at', 'question__question_text', 'answer__answer_text', 'response_type']
    list_filter = ['response_type']

@admin.register(SelfRecord)
class SelfRecordAdmin(admin.ModelAdmin):
    list_display = ['today', 'created_at', 'content']
    search_fields = ['today__created_at', 'content']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', 'question_subtype']
    search_fields = ['question_text', 'question_type__type_name', 'question_subtype__subtype_name']
    
@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'question_subtype', 'answer_code', 'answer_text']
    search_fields = ['question_subtype__subtype_name', 'answer_text']

admin.site.register(Today)
admin.site.register(QuestionType)
admin.site.register(QuestionSubtype)
