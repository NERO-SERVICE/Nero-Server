from django.contrib import admin
from .models import DrugList, ClinicLog

@admin.register(DrugList)
class DrugListAdmin(admin.ModelAdmin):
    list_display = ('id', 'drugName', 'capacity', 'unit')
    search_fields = ('drugName',)
    list_filter = ('capacity', 'unit')

@admin.register(ClinicLog)
class ClinicLogAdmin(admin.ModelAdmin):
    list_display = ('clinicId', 'drug', 'user', 'location', 'clinicDate', 'nextDate', 'doseTime', 'clinicNote')
    search_fields = ('drug__drugName', 'user__email', 'location')
    list_filter = ('clinicDate', 'nextDate', 'doseTime')
