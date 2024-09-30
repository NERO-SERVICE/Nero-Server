from django.contrib import admin
from .models import Menstruation

@admin.register(Menstruation)
class MenstruationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'startDate', 'endDate', 'cycleLength')
    search_fields = ('owner__username',)