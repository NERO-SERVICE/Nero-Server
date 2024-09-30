from django.contrib import admin
from fastlogs.models import DailyLog

# 빠른메모 관리
@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'content')
    list_filter = ('owner', 'date')
    search_fields = ('content',)
