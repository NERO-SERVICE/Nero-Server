from django.contrib import admin
from .models import Today, SurveyResponse, SideEffectResponse, SelfRecord, Question

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']
    

class SideEffectResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']


class SelfRecordAdmin(admin.ModelAdmin):
    list_display = ['today', 'created_at', 'content']
    search_fields = ['today__created_at', 'content']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type']
    search_fields = ['question_text', 'question_type']


admin.site.register(Today)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(SideEffectResponse, SideEffectResponseAdmin)
admin.site.register(SelfRecord, SelfRecordAdmin)
admin.site.register(Question, QuestionAdmin)
