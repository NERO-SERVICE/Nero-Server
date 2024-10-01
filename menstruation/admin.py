from django.contrib import admin
from .models import Menstruation

@admin.register(Menstruation)
class MenstruationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'startDate', 'endDate', 'display_cycleLength')
    search_fields = ('owner__username',)

    def display_cycleLength(self, obj):
        return obj.cycleLength
    display_cycleLength.short_description = '주기'
