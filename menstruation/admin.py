from django.contrib import admin
from .models import Menstruation

@admin.register(Menstruation)
class MenstruationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'startDate', 'endDate', 'cycleLength')
    search_fields = ('owner__username',)
    
    class Meta:
        app_label = "마이페이지"
        verbose_name = "생리주기"
        verbose_name_plural = "생리주기"
