from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount

class SocialAccountInline(admin.TabularInline):
    model = SocialAccount
    can_delete = False
    verbose_name_plural = 'social accounts'
    fields = ('provider', 'uid')

class CustomUserAdmin(UserAdmin):
    inlines = (SocialAccountInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'kakao_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'kakao_id')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'kakao_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
