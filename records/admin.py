from django.contrib import admin
from .models import QuestionList, ServeyLog, SymptomCare, SymptomLog

@admin.register(QuestionList)
class QuestionListAdmin(admin.ModelAdmin):
    list_display = ('questionId', 'type', 'content')
    search_fields = ('content', 'type')
    list_filter = ('type',)

@admin.register(ServeyLog)
class ServeyLogAdmin(admin.ModelAdmin):
    list_display = ('logId', 'questions', 'today', 'answer')
    search_fields = ('questions__content', 'answer')
    list_filter = ('today',)

@admin.register(SymptomCare)
class SymptomCareAdmin(admin.ModelAdmin):
    list_display = ('symptomId', 'type', 'content')
    search_fields = ('content', 'type')
    list_filter = ('type',)

@admin.register(SymptomLog)
class SymptomLogAdmin(admin.ModelAdmin):
    list_display = ('symptomLogId', 'symptomQuestions', 'today', 'answer')
    search_fields = ('symptomQuestions__content', 'answer')
    list_filter = ('today',)
