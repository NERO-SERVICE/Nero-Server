from django.contrib import admin
from .models import Mail

@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'short_suggestion')

    def short_suggestion(self, obj):
        return obj.suggestion[:50] + '...' if len(obj.suggestion) > 50 else obj.suggestion
    short_suggestion.short_description = "건의 내용"