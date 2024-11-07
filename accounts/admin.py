from django.contrib import admin
from .models import User, Memories
from django.utils import timezone
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'kakaoId', 'appleId', 'nickname', 'email', 
        'createdAt', 'birth', 'sex', 'is_product_writer', 
        'deleted_at', 'profile_image'
    ]
    search_fields = ['nickname', 'email']
    readonly_fields = ['id', 'createdAt']
    list_filter = ['deleted_at', 'is_product_writer']
    actions = ['soft_delete_users', 'restore_users']
    
    def get_queryset(self, request):
        return User.all_objects.all()
    
    def soft_delete_users(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        self.message_user(request, "Selected users have been soft deleted.")
    soft_delete_users.short_description = "Soft delete selected users"
    
    def restore_users(self, request, queryset):
        queryset.update(deleted_at=None)
        self.message_user(request, "Selected users have been restored.")
    restore_users.short_description = "Restore selected users"
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.deleted_at:
            return self.readonly_fields + ['nickname', 'email', 'sex', 'birth', 'profile_image']
        return self.readonly_fields

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.profile_image.url)
        return "No Image"
    profile_image_preview.short_description = 'Profile Image Preview'
    
    list_display += ('profile_image_preview',)
    

@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'get_user_nickname', 'items', 'deleted_at']
    search_fields = ['userId__nickname', 'items']
    readonly_fields = ['memoryId', 'deleted_at']
    
    def get_user_nickname(self, obj):
        return obj.userId.nickname
    
    get_user_nickname.short_description = 'User Nickname'
