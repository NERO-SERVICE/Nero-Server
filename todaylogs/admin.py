from django.contrib import admin
from .models import Today, SurveyResponse, SideEffectResponse, SelfRecord, Question

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "하루설문"
        verbose_name_plural = "하루설문"


class SideEffectResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "부작용설문"
        verbose_name_plural = "부작용설문"


class SelfRecordAdmin(admin.ModelAdmin):
    list_display = ['today', 'created_at', 'content']
    search_fields = ['today__created_at', 'content']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "셀프기록"
        verbose_name_plural = "셀프기록"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type']
    search_fields = ['question_text', 'question_type']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "질문모음"
        verbose_name_plural = "질문모음"


admin.site.register(Today)
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(SideEffectResponse, SideEffectResponseAdmin)
admin.site.register(SelfRecord, SelfRecordAdmin)
admin.site.register(Question, QuestionAdmin)
