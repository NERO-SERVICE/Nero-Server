from django.contrib import admin
from mypage.models import YearlyLog

@admin.register(YearlyLog)
class YearlyLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'log_type', 'action']
    list_filter = ['log_type', 'date']
    search_fields = ['owner__username', 'log_type']
