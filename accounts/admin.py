from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('kakaoId', 'nickname', 'is_active', 'is_staff')
