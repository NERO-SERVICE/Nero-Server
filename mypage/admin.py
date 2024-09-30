from django.contrib import admin
from mypage.models import YearlyDoseLog, YearlySideEffectLog
from menstruation.models import Menstruation

@admin.register(YearlyDoseLog)
class YearlyDoseLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'doseAction']


@admin.register(YearlySideEffectLog)
class YearlySideEffectLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'sideEffectAction']