from django.contrib import admin
from fastlogs.models import DailyLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'content']

    class Meta:
        app_label = "빠른메모"
        verbose_name = "빠른메모"
        verbose_name_plural = "빠른메모"
