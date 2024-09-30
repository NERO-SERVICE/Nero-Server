from django.contrib import admin
from todaylogs.models import Today, SurveyResponse, SideEffectResponse, SelfRecord, Question
from clinics.models import Clinics

# 하루기록 관리
@admin.register(Today)
class TodayAdmin(admin.ModelAdmin):
    pass

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']

@admin.register(SideEffectResponse)
class SideEffectResponseAdmin(admin.ModelAdmin):
    list_display = ['today', 'question', 'answer']
    search_fields = ['today__created_at', 'question__question_text', 'answer']

@admin.register(SelfRecord)
class SelfRecordAdmin(admin.ModelAdmin):
    list_display = ['today', 'created_at', 'content']
    search_fields = ['today__created_at', 'content']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type']
    search_fields = ['question_text', 'question_type']


# 진료기록 관리
@admin.register(Clinics)
class ClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'recentDay', 'description', 'createdAt', 'updatedAt']
    search_fields = ['description', 'owner__username']
    list_filter = ['createdAt', 'updatedAt', 'owner']
