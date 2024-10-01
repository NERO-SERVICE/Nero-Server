from django.contrib import admin
from .models import Today, SurveyResponse, SideEffectResponse, SelfRecord, Question, QuestionType, QuestionSubtype, AnswerChoice

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer__answer_text']


class SideEffectResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer__answer_text']


class SelfRecordAdmin(admin.ModelAdmin):
    list_display = ['today', 'created_at', 'content']
    search_fields = ['today__created_at', 'content']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type', 'question_subtype']
    search_fields = ['question_text', 'question_type__type_name', 'question_subtype__subtype_name']
    
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ['question_subtype', 'answer_code', 'answer_text']
    search_fields = ['question_subtype__subtype_name', 'answer_text']

admin.site.register(Today)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(SideEffectResponse, SideEffectResponseAdmin)
admin.site.register(SelfRecord, SelfRecordAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionType)
admin.site.register(QuestionSubtype)
admin.site.register(AnswerChoice, AnswerChoiceAdmin)