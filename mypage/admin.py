from django.contrib import admin
from mypage.models import YearlyDoseLog, YearlySideEffectLog
from menstruation.models import Menstruation

@admin.register(YearlyDoseLog)
class YearlyDoseLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'doseAction']

    class Meta:
        app_label = "마이페이지"
        verbose_name = "연간관리 - 약복용"
        verbose_name_plural = "연간관리 - 약복용"


@admin.register(YearlySideEffectLog)
class YearlySideEffectLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'sideEffectAction']

    class Meta:
        app_label = "마이페이지"
        verbose_name = "연간관리 - 부작용"
        verbose_name_plural = "연간관리 - 부작용"