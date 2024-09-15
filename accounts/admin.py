from django.contrib import admin
from .models import User, Memories

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'kakaoId', 'nickname', 'email', 'createdAt', 'birth', 'sex']
    search_fields = ['nickname', 'email']

@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'userId__nickname', 'items']
    search_fields = ['userId__nickname', 'items']
