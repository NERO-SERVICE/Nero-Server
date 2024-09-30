from django.contrib import admin
from .models import DailyLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'content')
    list_filter = ('owner', 'date')
    search_fields = ('content',)

    class Meta:
        app_label = "빠른메모"
        verbose_name = "빠른메모"
        verbose_name_plural = "빠른메모"
