from django.contrib import admin
from .models import YearlyDoseLog, YearlySideEffectLog

@admin.register(YearlyDoseLog)
class YearlyDoseLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'doseAction']
    search_fields = ['owner__username', 'date']
    list_filter = ['doseAction', 'date']


@admin.register(YearlySideEffectLog)
class YearlySideEffectLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'sideEffectAction']
    search_fields = ['owner__username', 'date']
    list_filter = ['sideEffectAction', 'date']
