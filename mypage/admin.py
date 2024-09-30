from django.contrib import admin
from mypage.models import YearlyDoseLog, YearlySideEffectLog
from menstruation.models import Menstruation

# 마이페이지 관리
@admin.register(YearlyDoseLog)
class YearlyDoseLogAdmin(admin.ModelAdmin):
    pass

@admin.register(YearlySideEffectLog)
class YearlySideEffectLogAdmin(admin.ModelAdmin):
    pass


# 생리주기 관리
@admin.register(Menstruation)
class MenstruationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'startDate', 'endDate', 'cycleLength')
    search_fields = ('owner__username',)
