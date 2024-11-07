from django.contrib import admin
from .models import User, Memories, ProfileImage
from django.utils import timezone

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'kakaoId', 'appleId', 'nickname', 'email', 'createdAt', 'birth', 'sex', 'is_product_writer', 'deleted_at']
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
            return self.readonly_fields + ['nickname', 'email', 'sex', 'birth']
        return self.readonly_fields
    
@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
    search_fields = ['user__nickname']
    readonly_fields = ['user']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    

@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'get_user_nickname', 'items', 'deleted_at']
    search_fields = ['userId__nickname', 'items']
    readonly_fields = ['memoryId', 'deleted_at']
    
    def get_user_nickname(self, obj):
        return obj.userId.nickname
    
    get_user_nickname.short_description = 'User Nickname'
