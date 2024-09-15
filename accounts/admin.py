from django.contrib import admin
from .models import User, Memories

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'kakaoId', 'nickname', 'email', 'createdAt', 'birth', 'sex']
    search_fields = ['nickname', 'email']

@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'get_user_nickname', 'items']
    search_fields = ['userId__nickname', 'items']

    def get_user_nickname(self, obj):
        return obj.userId.nickname
    
    get_user_nickname.short_description = 'User Nickname'
