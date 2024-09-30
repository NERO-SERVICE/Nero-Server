from django.contrib import admin
from .models import Mail

@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'suggestion')
    
    class Meta:
        app_label = "유저관리"
        verbose_name = "개발자 건의함"
        verbose_name_plural = "개발자 건의함"
